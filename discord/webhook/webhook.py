import boto3
import botocore
import pandas as pd
import json
from discordwebhook import Discord
from datetime import datetime, timedelta
import time
import os


DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
BUCKET_NAME = 'automatizacion-uni-2024' # replace with your bucket name
TABLE_NAME = 'Automatizacion-discord-config'

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

def filter_dataset(json_dataset, source, sport):

    df = pd.DataFrame(json_dataset)
    if (source != "No") and (sport != "No"):
        condiciones = (df['news source'] == source) & (df['sport'] == sport)
        df = df[condiciones]
    elif (source != "No"):
        condiciones = (df['news source'] == source)
        df = df[condiciones]
    elif (sport != "No"):
        condiciones =  (df['sport'] == sport)
        df = df[condiciones]

    fila_elegida = df.sample()
    print(fila_elegida)
    return (fila_elegida["title"].values[0],
    fila_elegida["description"].values[0],
    fila_elegida["news source"].values[0],
    fila_elegida["sport"].values[0],
    fila_elegida["link"].values[0]
    )

def upload_to_database(nombre_server,fuente, deporte, frecuencia):

    dynamodb = boto3.resource('dynamodb')
    frecuencia = int(frecuencia)
    table = dynamodb.Table(TABLE_NAME)
    TTL = datetime.now() + timedelta(hours=frecuencia)

    TTL = int(time.mktime(TTL.timetuple()))
    table.put_item(
        Item={
            # PK
            'server_name': nombre_server,
            'source': fuente,
            'sport': deporte,
            'frequency': frecuencia,
            'created_at': str(datetime.now()),
            'TTL': TTL,
            'Active': True
        }
    )

def lambda_handler(event, context):
    print("event", event)

    dynamodb = ""
    def log_dynamodb_record(record):
        print(record['eventID'])
        print(record['eventName'])
        print(f"DynamoDB Record: {json.dumps(record['dynamodb'])}")

    for record in event['Records']:
        log_dynamodb_record(record)
        if record['eventName'] != "REMOVE":
            return False
        dynamodb = record['dynamodb']

    dynamodbOld= dynamodb['OldImage']
    # dynamodbOld= dynamodb['NewImage']

    server_name = dynamodbOld['server_name']['S']
    Active = dynamodbOld["Active"]['BOOL']
    created_at = dynamodbOld["created_at"]['S']
    source = dynamodbOld["source"]['S']
    sport = dynamodbOld["sport"]['S']
    frequency = dynamodbOld["frequency"]['N']
    print(server_name,Active,created_at,source,sport,frequency)


    filename = get_file_name()
    print('filename', filename)
    json_dataset = get_dataset_json(filename)
    titulo, descripcion, fuente, deporte, link = filter_dataset(json_dataset, source,sport)
    mensaje = (
            "\n ESTAS SON TUS NOTICIAS DE HOY \n"
            f"Título: {titulo}\n"
            f"Descripción: {descripcion}\n"
            f"Fuente de noticias: {fuente}\n"
            f"Deporte: {deporte}\n"
            f"{link}\n"
            "------------------------------------"
        )

    upload_to_database(server_name,source, sport, frequency)

    # # DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
    discord = Discord(url=DISCORD_WEBHOOK)
    discord.post(content=mensaje)

