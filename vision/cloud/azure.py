import os
import requests

AZURE_API_ENDPOINT = os.getenv('AZURE_CLOUD_VISION_ENDPOINT')
AZURE_ACCESS_KEY1 = os.getenv('AZURE_CLOUD_VISION_KEY1')
AZURE_ACCESS_KEY2 = os.getenv('AZURE_CLOUD_VISION_KEY2')


def get_image_tags(image):
    """Return image information."""
    url = AZURE_API_ENDPOINT + '/analyze'
    params = {'visualFeatures': 'Description'}
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': AZURE_ACCESS_KEY1,
    }
    data = {}

    try:
        response = requests.post(url, params=params, data=image, headers=headers)
        data = response.json()
    finally:
        return data
