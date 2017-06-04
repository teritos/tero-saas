import os
import logging
import requests

AZURE_API_ENDPOINT = os.getenv('AZURE_API_ENDPOINT')
AZURE_ACCESS_KEY1 = os.getenv('AZURE_ACCESS_KEY1')
logger = logging.getLogger('vision')


def find_humans_on(image):
    """Find humans on image."""
    found_tags = []
    positive_tags = ['man', 'person', 'woman', 'people', 'young']
    metadata = get_image_tags(image)
    if not metadata:
        return found_tags
    tags = metadata['description']['tags']
    for tag in tags:
        if tag in positive_tags:
            found_tags.append(tag)
    return found_tags


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
    except Exception as exc:
        logger.exception('Error en Azure Vision API.')
    finally:
        return data
