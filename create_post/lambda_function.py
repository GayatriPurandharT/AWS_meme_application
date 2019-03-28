import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('posts')
user_table = dynamodb.Table('gusers')
sns = boto3.resource('sns')

def get_user_sns(user_id):
    response = user_table.get_item(Key={
        'id': int(user_id)
    })
    if 'Item' in response:
        return response['Item']['sns_arn']
    else:
        return None

def publish(post):
    user_id = post['user_info']['id']
    sns_arn = get_user_sns(user_id)
    topic = sns.Topic(sns_arn)
    subject = 'You have a new articel from ' + post['user_info']['name']
    message = 'Title: ' + post['title']
    response = topic.publish(
        Message=message,
        Subject=subject
    )

def put_post(post_info):
    response = table.put_item(
       Item=post_info
    )

def lambda_handler(event, context):
    put_post(event)
    publish(event)
    return {
        'statusCode': 200
    }

