import boto3, os
from dotenv import load_dotenv

load_dotenv()
session = boto3.Session(
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name = 'us-west-2'
)
s3 = session.resource("s3")

s3.Bucket('scraperak').upload_file('test.txt', 'screenshots/test.txt')