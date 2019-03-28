import json
import boto3

dynamodb = boto3.resource('dynamodb')
sns = boto3.resource('sns')

table = dynamodb.Table('gusers')

def get_user_sns(user_id):
    response = table.get_item(Key={
        'id': int(user_id)
    })
    if 'Item' in response:
        return response['Item']['sns_arn']
    else:
        return None

def subscribe(target_user_id, user_info):
    sns_arn = get_user_sns(target_user_id)
    topic = sns.Topic(sns_arn)
    subscription = topic.subscribe(
        Protocol='email',
        Endpoint=user_info['email'],
        ReturnSubscriptionArn=True
    )
    return subscription.arn

def add_sub_arn(sub_arn, user_info):
    response = table.update_item(
        Key={
            'id': int(user_info['id'])
        },
        UpdateExpression="SET subscriptions = list_append(subscriptions, :sub_arn)",
        ExpressionAttributeValues={
            ':sub_arn': [sub_arn]
        }
    )

def lambda_handler(event, context):
    target_user_id = event['target_user_id']
    user_info = event['user_info']
    subscription_arn = subscribe(target_user_id, user_info)
    add_sub_arn(subscription_arn, user_info)
    return {
        'statusCode': 200
    }

