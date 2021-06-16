import boto3
from dotenv import dotenv_values

#load .env config
config = dotenv_values("../key/.env")

s3 = boto3.client('s3',
                  aws_access_key_id = config["AWS_ACCESS_KEY"],
                  aws_secret_access_key= config["AWS_SECRET_KEY"],
                  # aws_session_token='secret token here' #only temporary credential needed
                 )
BUCKET_NAME = config["S3_BUCKET_NAME"]