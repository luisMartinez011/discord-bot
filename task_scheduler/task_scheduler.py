from datetime import datetime, timedelta
import boto3
import time
from boto3.dynamodb.conditions import Key,Attr
import json

class TaskScheduler():

    table_name = 'Automatizacion-discord-config'
    dynamodb = boto3.resource('dynamodb')

    def __init__(self, fuente = 'AS', deporte = 'Basquetbol', frecuencia = 1,nombre_server = 'T1'):

        #? Las fuentes de noticias seran las siguientes:
        #? Espn
        #? AS
        #? Fansided
        self.fuente = fuente

        #? Los deportes sera
        #? Futbol
        #? Beisbol
        #? Basquetbol
        self.deporte = deporte

        # ? La frecuencia sera en horas
        # ? Example: 6 horas

        self.frecuencia = frecuencia

        # ? El nombre del server donde se hace la configuracion
        self.nombre_server = nombre_server


    def upload_to_database(self):
        dynamodb = self.dynamodb

        table = dynamodb.Table(self.table_name)
        TTL = datetime.now() + timedelta(minutes=self.frecuencia)

        TTL = int(time.mktime(TTL.timetuple()))
        table.put_item(
            Item={
                # PK
                'server_name': self.nombre_server,
                'source': self.fuente,
                'sport': self.deporte,
                'frequency': self.frecuencia,
                'created_at': str(datetime.now()),
                'TTL': TTL,
                'Active': True
            }
        )

    # TODO: Eliminar esta funcion al final por si no se usa
    def return_latest_configuration(self):
        dynamodb = self.dynamodb

        table = dynamodb.Table(self.table_name)

        response = table.query(
            KeyConditionExpression=Key('server_name').eq(self.nombre_server),
            FilterExpression=Attr('Active').eq(True)

        )

        print(response['Items'])

def lambda_handler(event, context):
    body =json.loads(event.get("body"))
    fuente = body["fuente"]
    deporte = body["deporte"]
    frecuencia = body["frecuencia"]
    nombre_server = body["nombre_server"]

    taskScheduler = TaskScheduler(fuente, deporte , frecuencia, nombre_server)
    taskScheduler.upload_to_database()
