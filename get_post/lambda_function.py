import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('posts')
user_table = dynamodb.Table('gusers')

def get_user_subscriptions(user_id):
    response = user_table.get_item(Key={
        'id': int(user_id)
    })
    if 'Item' in response:
        return response['Item']['subscriptions']
    else:
        return None

def get_from_table(post_id):
    response = table.get_item(Key={
        'id': int(post_id)
    })
    if 'Item' in response:
        post = response['Item']
    else:
        post = None
    return post

def is_subscribed(author_id, subscription_arns):
    for subscription_arn in subscription_arns:
        if author_id in subscription_arn:
            return True
    return False
    
def lambda_handler(event, context):
    post = get_from_table(event['post_id'])
    author_id = str(post['user_info']['id'])
    user_id = event['user_info']['id']
    subscription_arns = get_user_subscriptions(user_id)
    post['is_subscribed'] = is_subscribed(author_id, subscription_arns)
    return {
        'statusCode': 200,
        'body': post
    }

