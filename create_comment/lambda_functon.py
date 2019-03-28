import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('posts')

def put_comment(comment_info):
    post_id = comment_info['post_id']
    comment = comment_info['comment']
    response = table.update_item(
        Key={
            'id': int(post_id)
        },
        UpdateExpression="SET comments = list_append(comments, :comment)",
        ExpressionAttributeValues={
            ':comment': [comment]
        }
    )
    print(response)

def lambda_handler(event, context):
    put_comment(event)
    return {
        'statusCode': 200
    }

