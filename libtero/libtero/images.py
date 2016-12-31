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


def make_hash(fname, hashfunc=imagehash.dhash):
    """Make image hash."""
    img = Image.open(fname)
    return hashfunc(img)


def load_hash(string):
    """Load image hash from string."""
    return imagehash.hex_to_hash(string)


def compare_hash(hash1, hash2):
    """Returns a float between 0-1 on how similar given images are.
    1 means images are the same, 0 means images are totally different.
    Hamming distance goes from 0-64 bits.
    """

    distance = hash1 - hash2
    score = 1 - distance / 64.0
    return score
