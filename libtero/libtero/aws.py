import boto3
import botocore

try:
    rekognition = boto3.client('rekognition')
except botocore.exceptions.BotoCoreError:
    rekognition = None
