import boto3
import json
import requests

# Creating an S3 client
s3 = boto3.client('s3', region_name='us-east-1')

# Creating a new S3 bucket
bucket_name = 'music-app-images'
s3.create_bucket(Bucket=bucket_name)

# Loading data from a1.json
with open('a1.json') as file:
    data = json.load(file)
    for song in data['songs']:
        image_url = song['img_url']
        image_name = image_url.split('/')[-1]

        # Downloading the image
        response = requests.get(image_url)
        image_data = response.content

        # Uploading the image to S3
        s3.put_object(Bucket=bucket_name, Key=image_name, Body=image_data)