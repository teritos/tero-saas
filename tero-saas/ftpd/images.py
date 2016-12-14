from pathlib import (
    Path,
    PurePath
)
from itertools import tee
from multiprocessing import Process
from tero.deep import run_detector
from tero.images import compare
from settings.asgi import channel_layer
from alarm.models import (
    AlarmImage,
    Alarm
)
import logging
import os


SIMILAR_IMGS_BARRIER = 0.80
logger = logging.getLogger("ftpd")


class ImageHandler(object):

    def _pairwise(self, iterator):
        a, b = tee(iterator)
        next(b, None)
        return zip(a, b)

    def get_files_to_check(self, filepath):
        path = PurePath(filepath)

        # Get all the images from the last 10 seconds
        stem = path.stem[:-3] + '*.*.jpg'
        im10list = sorted(Path(path.parent).glob(stem))
        _stem = None
        to_check = []
        for im in im10list:
            if im.stem[:-2] == _stem:  # ignore same second images
                continue
            _stem = im.stem[:-2]
            to_check.append(im)

        return to_check

    def set_similar_score(self, files_to_check):
        scores = []
        if len(files_to_check) == 1:
            scores.append((files_to_check[0], files_to_check[0], 0))
            return scores

        for x, y in self._pairwise(files_to_check):
            scores.append((x, y, compare(x, y)))

        return scores 

    def analyze_image(self, imgpath, username):
        pid = os.getpid()
        logger.info('Pid %s >>> Going to run detector on %s', pid, imgpath.name)
        predicted = run_detector(imgpath.as_posix())
        logger.info('Pid %s >>> Detector finished on %s, it tooks %s', pid, imgpath.name, predicted['ptime'])
        if predicted['person_detected']:
            logger.info(
                'Person detected on %s, prediction saved on %s, detected %s',
                imgpath.name, str(predicted['saved']), predicted['labels']
            )
            alarm = Alarm.get_by_username(username)
            alarm_image = AlarmImage(alarm=alarm, image=str(predicted['saved']))
            alarm_image.save()
            channel_layer.send('messenger.telegram', {
                'text': 'Persona detectada.',
                'username': username,
                'filepath': str(predicted['saved']),
            })
            logger.info("Pid %s >>> Saved image on DB. Alarm id %s", pid, alarm_image.id)

    def handle(self, filepath, username):
        files_to_check = self.get_files_to_check(filepath)
        scores = self.set_similar_score(files_to_check)
        for score in scores:
            img_a, img_b, diff = score
            if diff >= SIMILAR_IMGS_BARRIER:
                continue
            logger.info('%s differs %s with %s', img_b.name, diff, img_a.name)
            logger.info('Checking labels on %s', img_b.name)
            p = Process(target=self.analyze_image, args=(img_b, username))
            p.start()
            p.join()

