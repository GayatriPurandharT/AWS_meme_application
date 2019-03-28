import json
import boto3

dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

table = dynamodb.Table('gusers')

def is_user_exsit(user_info):
    response = table.get_item(Key={
        'id': int(user_info['id'])
    })
    return 'Item' in response

def create_sns(user_info):
    topic_name = str(user_info['id']) + '-' + user_info['given_name']
    response = sns_client.create_topic(
        Name=topic_name
    )
    return response['TopicArn']

def put_user(user_info):
    user_info['id'] = int(user_info['id'])
    response = table.put_item(
       Item=user_info
    )

def lambda_handler(event, context):
    user_info = event
    if not is_user_exsit(user_info):
        sns_arn = create_sns(user_info)
        user_info['sns_arn'] = sns_arn
        put_user(user_info)
    return {
        'statusCode': 200
    }

