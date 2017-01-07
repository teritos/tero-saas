"""Amazon rekognition utility."""
import boto3
from .aws import rekognition as aws_rekognition


class S3Image(object):
    """Simple object to represent an image to be stored on S3."""

    def __init__(self, bucket, name):
        self.bucket = bucket
        self.name = name


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
        response = aws_rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': image.bucket,
                    'Name': image.name,
                }
            },
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )

    if response:
        labels = response['Labels']

    return labels
