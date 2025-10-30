import boto3
import json
import os
import uuid
from datetime import datetime

def lambda_handler(event,context):
    print(f"Received event: {json.dumps(event)}")

    if "body" not in event or event["httpMethod"] != "POST":
        return {
            "statusCode": 400,
            "body": json.dumps({"msg": "Bad Request"})
        }
    table_name = os.environ.get("TABLE", "Todos")
    region = os.environ.get("AWS_REGION", "us-east-1")
    aws_environment = os.environ.get("AWSENV", "AWS")

    if aws_environment == "AWS_SAM_LOCAL":
        todo_table = boto3.resource(
            "dynamodb",
            endpoint_url="http://dynamodb:8000"
        )
    else:
        todo_table = boto3.resource(
            "dynamodb", region_name=region
        )

    table = todo_table.Table(table_name)
    todo = json.loads(event["body"])

    params = {
        'todo_id': str(uuid.uuid4()),
        'created_at': str(datetime.timestamp(datetime.now())),
        'title': todo["title"],
        'status': todo["status"],
    }

    response = table.put_item(
        TableName=table_name,
        Item=params
    )

    print(f"response: {response}")

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'msg': 'Todo created'})
    }