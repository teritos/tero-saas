"""Utils to process images."""
import imagehash

from skimage.measure import compare_ssim as _compare_ssim
from skimage.io import imread
from PIL import Image


def compare_ssim(fname_a, fname_b):
    """Returns a float between 0-1 on how similar given images are.
    1 means images are the same, 0 means images are totally different.

        Arguments:
            fname_a (FilePath)      Image Filepath 1
            fname_b (FilePath)      Image Filepath 2

        Usage:

            >>> from tero.images import compare

            >>> compare('a.jpg', 'b.jpg')
            0.90009695173409698

    """
    img_a = imread(fname_a, as_grey=True)
    img_b = imread(fname_b, as_grey=True)
    ssi = _compare_ssim(img_a, img_b)

    return ssi


class ImageHash(object):
    """
    imagehash Wrapper
    """

    def __init__(self, filepath=None, hashfunc=imagehash.dhash):
        if not filepath:
            return
        img = Image.open(filepath)
        self.hash = hashfunc(img)

    def compare(self, other):
        """Returns a float between 0-1 on how similar given images are.
        1 means images are the same, 0 means images are totally different.
        Hamming distance goes from 0-64 bits.
        """

        distance = self.hash - other.hash
        score = 1 - distance / 64.0
        return score

    @classmethod
    def from_string(cls, value):
        new = cls()
        new.hash = imagehash.hex_to_hash(value)
        return new

    def __str__(self):
        return str(self.hash)