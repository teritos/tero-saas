import os
import logging
import redis
from multiprocessing import Process

from libtero.deep import run_detector
from libtero.images import make_hash, load_hash, compare_hash
from alarm.models import (
    AlarmImage,
    Alarm
)


logger = logging.getLogger("ftpd")

# redis client
r = redis.StrictRedis()


class ImageHandler(object):

    def analyze(self, filepath, username):
        pid = os.getpid()
        logger.info('Pid %s >>> Going to run detector on %s', pid, filepath)
        predicted = run_detector(filepath)
        logger.info('Pid %s >>> Detector finished on %s, it tooks %s', pid, filepath, predicted['ptime'])
        if predicted['person_detected']:
            logger.info(
                'Person detected on %s, prediction saved on %s, detected %s',
                filepath, str(predicted['saved']), predicted['labels']
            )
            alarm = Alarm.get_by_username(username)
            alarm_image = AlarmImage(alarm=alarm, image=str(predicted['saved']))
            alarm_image.save()
            logger.info("Pid %s >>> Saved image on DB. Alarm id %s", pid, alarm_image.id)

    def handle(self, filepath, username):
        MOTION_TTL = os.getenv('MOTION_TTL', 60) # seconds
        SIMILARITY = os.getenv('SIMILAR_IMGS_BARRIER', 0.8)

        image_hash = make_hash(filepath)
        key = 'motion.{}'.format(username)

        # first image
        if not r.exists(key):
            r.set(key, str(image_hash), MOTION_TTL)

        # inside MOTION_TTL
        else:
            last = r.get(key).decode('ascii')
            last_hash = load_hash(last)

            ttl = r.ttl(key)
            r.set(key, str(image_hash), ttl)

            score = compare_hash(image_hash, last_hash)

            logger.info("{} / SIMILARITY: {}".format(score, SIMILARITY))

            if score > SIMILARITY:
                return

        logger.info('Checking labels on %s', filepath)

        p = Process(target=self.analyze, args=(filepath, username))
        p.start()
        p.join()
