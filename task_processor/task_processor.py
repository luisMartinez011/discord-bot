import boto3
import botocore
import json
import pandas as pd

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

def filter_dataset(json_dataset, source="No", sport="No"):

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

    print("df: ", df)
    fila_elegida = df.sample()
    print(fila_elegida)
    return (fila_elegida["title"].values[0],
    fila_elegida["description"].values[0],
    fila_elegida["news source"].values[0],
    fila_elegida["sport"].values[0],
    fila_elegida["link"].values[0]
    )

#TODO: implementar despues este codigo
def lambda_handler(event, context):
    filename = get_file_name()
    json_file = get_dataset_json(filename)
    titulo, descripcion, fuente, deporte, link = filter_dataset(json_file, "As", "No")
    print(titulo, descripcion, fuente, deporte, link )
    mensaje = (
            "\n ESTAS SON TUS NOTICIAS DE HOY \n"
            f"Título: {titulo}\n"
            f"Descripción: {descripcion}\n"
            f"Fuente de noticias: {fuente}\n"
            f"Deporte: {deporte}\n"
            f"{link}\n"
            "------------------------------------"
        )
    print(mensaje)
    return "Bot de discord ejecutandose"

lambda_handler("event","efdfg")
