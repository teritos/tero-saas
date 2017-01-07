import os
import logging
import redis
from multiprocessing import Process

from libtero.deep import run_detector
from alarm.models import (
    AlarmImage,
    Alarm
)


logger = logging.getLogger("ftpd")

# redis client
r = redis.StrictRedis()

MOTION_TTL = os.getenv('MOTION_TTL', 60) # seconds
SIMILARITY_THRESHOLD = os.getenv('SIMILARITY_THRESHOLD', 0.8)


class ImageHandler(object):

    def __init__(self, filepath=None, username=None):
        self.filepath = filepath
        self.username = username

    def is_similar(self):
        image_hash = ImageHash(filepath=self.filepath)
        key = 'motion.{}'.format(self.username)

        # first image
        if not r.exists(key):
            r.set(key, str(image_hash), MOTION_TTL)

        # inside MOTION_TTL
        else:
            last_value = r.get(key).decode('ascii')
            last_hash = ImageHash.from_string(last_value)

            ttl = r.ttl(key)
            r.set(key, str(image_hash), ttl)

            score = image_hash.compare(last_hash)

            logger.info("{} / SIMILARITY_THRESHOLD: {}".format(score, SIMILARITY_THRESHOLD))

            if score > SIMILARITY_THRESHOLD:
                return True

        return False
    
    def analyze(self):
        pid = os.getpid()
        logger.info('Pid %s >>> Going to run detector on %s', pid, self.filepath)
        predicted = run_detector(self.filepath)
        logger.info('Pid %s >>> Detector finished on %s, it tooks %s', pid, self.filepath, predicted['ptime'])
        if predicted['person_detected']:
            logger.info(
                'Person detected on %s, prediction saved on %s, detected %s',
                self.filepath, str(predicted['saved']), predicted['labels']
            )
            alarm = Alarm.get_by_username(self.username)
            alarm_image = AlarmImage(alarm=alarm, image=str(predicted['saved']))
            alarm_image.save()
            logger.info("Pid %s >>> Saved image on DB. Alarm id %s", pid, alarm_image.id)
