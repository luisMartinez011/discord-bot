import boto3
from pprint import pprint
from boto3.dynamodb.conditions import Key


table_name = "Automatizacion-discord-dataset"
dynamodb = boto3.resource("dynamodb")
orders_table = dynamodb.Table(table_name)

def query_data_with_sort():
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

    print(response["Items"])

query_data_with_sort()
