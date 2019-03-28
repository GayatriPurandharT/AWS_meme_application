import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('posts')

def list_from_table():
    response = table.scan()
    posts = {"items": response['Items']}
    return posts
  
def lambda_handler(event, context):
    posts = list_from_table()
    return {
        'statusCode': 200,
        'body': posts
    }

