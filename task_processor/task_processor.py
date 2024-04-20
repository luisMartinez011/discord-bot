import boto3
import botocore
import json

def get_file_name():
    table_name = "Automatizacion-discord-dataset"
    dynamodb = boto3.resource("dynamodb")
    orders_table = dynamodb.Table(table_name)

    # sorts items in descending order based on sort key when ScanIndexForward=False
    # sorts items in ascending order based on sort key when ScanIndexForward=True which is default
    response = orders_table.query(
        KeyConditionExpression="dataset_id = :id",
        ExpressionAttributeValues={
            ":id": "1",
        },
        ScanIndexForward=False,
        Limit=1
    )

    # print(response["Items"][0]["file_name"])
    file_name = response["Items"][0]["file_name"]
    return file_name

def get_dataset_json(KEY):
    BUCKET_NAME = 'automatizacion-uni-2024' # replace with your bucket name

    s3 = boto3.client('s3')
    try:
        # Retrieve the JSON file from S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
        json_content = json.loads(response['Body'].read())
        return json_content
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

#TODO: implementar despues este codigo
def lambda_handler(event, context):
    filename = get_file_name()
    json_file = get_dataset_json(filename)
    return "Bot de discord ejecutandose"
