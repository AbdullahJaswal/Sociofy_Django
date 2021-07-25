import boto3
from celery import shared_task

from aws_configs import *


@shared_task
def getSentiment(id, text):
    comprehend = boto3.client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        service_name='comprehend',
        region_name='ap-southeast-1'
    )

    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    return {"id": id, "sentiment": sentiment.get("Sentiment")} or None
