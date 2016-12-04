import boto3
from .aws import rekognition 
from skimage.io import imread
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


def compare(fname_a, fname_b):
    """Returns a float between 0-1 on how different given images are.
    1 means images are the same, 0 means images are totally different.

        Arguments:
            fname_a (FilePath)      Image Filepath 1
            fname_b (FilePath)      Image Filepath 2

        Usage:

            >>> from tero.images import compare

            >>> compare('a.jpg', 'b.jpg')
            0.90009695173409698

    """

    # TODO
    # Handle / compare S3Images

    img_a = imread(fname_a, as_grey=True)
    img_b = imread(fname_b, as_grey=True)
    ssi = ssim(img_a, img_b)

    return ssi
