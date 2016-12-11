from pathlib import (
    Path,
    PurePath
)
from itertools import tee
from tero.images import compare
import logging


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
            scores.append(files_to_check[0], 0)
            return scores

        for x, y in self._pairwise(files_to_check):
            scores.append((x, y, compare(x, y)))

        return scores 

    def handle(self, filepath):
        files_to_check = self.get_files_to_check(filepath)
        scores = self.set_similar_score(files_to_check)
        for score in scores:
            img_a, img_b, diff = score
            print('%s\t%s\t%s' % (img_a.name, img_b.name, diff))
