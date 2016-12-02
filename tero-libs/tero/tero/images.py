import boto3
import numpy as np 
from .aws import rekognition 
from scipy.misc import imread
from skimage import img_as_float
from skimage.measure import compare_mse as mse
from skimage.measure import compare_ssim as ssim


class S3Image(object):

    def __init__(self, bucket, name):
        self.Bucket = bucket
        self.Name = name


def detect_labels(image, max_labels=5, min_confidence=80):
    """Return a dict with detected labels on Image.

        Arguments:
            image (object)              - Can be an S3Image, FilePath, etc.
            max_labels (default=5)      - How many labels you want back
            min_confidence (default=80) - Return only labels that have >= 
                                          specified confidence
    
        Usage:

            >>> from tero.images import S3Image, detect_labels

            >>> bucket = 'tero-test'

            >>> image = S3Image(bucket, '1.jpg')

            >>> detect_labels(image, max_labels=2)
            [{'Confidence': 98.7676773071289, 'Name': 'People'},
             {'Confidence': 98.7677001953125, 'Name': 'Person'}]

    """
    
    response = None 
    labels = []

    if isinstance(image, S3Image):
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': image.Bucket,
                    'Name': image.Name,
                }
            },
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )

    if response:
        labels = response['Labels']

    return labels 


def to_grayscale(image_path):
    return imread(image_path).astype(float)


def compare(image_a, image_b):
    """Compare two images."""


def detect_person(image_path):
    """Return bool if a person is detected on given image."""
