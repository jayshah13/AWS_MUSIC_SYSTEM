import boto3
import json

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Creating the 'login' table with sample data
login_table_name = 'login'
login_table = dynamodb.create_table(
    TableName=login_table_name,
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Waiting until the table exists
login_table.meta.client.get_waiter('table_exists').wait(TableName=login_table_name)

# login data to be added
login_data = [
    {"email": "s3000008@student.rmit.edu.au", "password": "890123", "user_name": "Firstname Lastname8"},
    {"email": "s3000009@student.rmit.edu.au", "password": "901234", "user_name": "Firstname Lastname9"},
    {"email": "s3000007@student.rmit.edu.au", "password": "789012", "user_name": "Firstname Lastname7"},
    {"email": "s3000004@student.rmit.edu.au", "password": "456789", "user_name": "Firstname Lastname4"},
    {"email": "s3000001@student.rmit.edu.au", "password": "123456", "user_name": "Firstname Lastname1"},
    {"email": "s3000006@student.rmit.edu.au", "password": "678901", "user_name": "Firstname Lastname6"},
    {"email": "s3000005@student.rmit.edu.au", "password": "567890", "user_name": "Firstname Lastname5"},
    {"email": "s3000003@student.rmit.edu.au", "password": "345678", "user_name": "Firstname Lastname3"},
    {"email": "s3000000@student.rmit.edu.au", "password": "012345", "user_name": "Firstname Lastname0"},
    {"email": "s3000002@student.rmit.edu.au", "password": "234567", "user_name": "Firstname Lastname2"}
]

# Loading login data into the 'login' table
with login_table.batch_writer() as batch:
    for item in login_data:
        batch.put_item(Item=item)

# Creating the 'music' table
music_table_name = 'music'
music_table = dynamodb.create_table(
    TableName=music_table_name,
    KeySchema=[
        {
            'AttributeName': 'title',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'artist',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'artist',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Waiting until the table exists
music_table.meta.client.get_waiter('table_exists').wait(TableName=music_table_name)

# Loading data from a1.json into the 'music' table
with open('a1.json') as file:
    data = json.load(file)
    with music_table.batch_writer() as batch:
        for song in data['songs']:
            item = {
                'title': song['title'],
                'artist': song['artist'],
                'year': song['year'],
                'web_url': song['web_url'],
                'image_url': song['img_url']
            }
            batch.put_item(Item=item)

# Creating the 'subscription' table for main.py
subscription_table_name = 'subscription'
subscription_table = dynamodb.create_table(
    TableName=subscription_table_name,
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'title',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Waiting until the table exists
subscription_table.meta.client.get_waiter('table_exists').wait(TableName=subscription_table_name)