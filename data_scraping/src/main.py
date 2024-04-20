### AS
from as_scraper import AsScrapper
from espn_scraper import EspnScrapper
from fansided_scraper import FansidedScrapper
from datetime import datetime
import pandas as pd
import boto3
# import os
# from dotenv import load_dotenv
# load_dotenv()

def lambda_handler(event, context):

    news_df = pd.DataFrame(columns=['title', 'description', 'link', 'image','news source', 'sport'])


    ###As
    news_source = "As"
    urls = {
        # 'Futbol': "https://mexico.as.com/futbol/?omnil=mpal",
        'Basquetbol': "https://mexico.as.com/noticias/nba/",
        # 'Beisbol': "https://mexico.as.com/noticias/beisbol"
    }


    for sport, url in urls.items():

        web_scrapper = AsScrapper(url, news_source, sport)
        html = web_scrapper.fetch_html()
        arr = web_scrapper.analyze_html(html)
        if arr.empty:
            raise ValueError("No news collected")
        news_df= pd.concat([arr, news_df], ignore_index=True)

    # Fansided
    news_source = "Fansided"

    # urls = {
    #     'Futbol': "https://fansided.com/es/leagues/futbol",
    #     'Basquetbol': "https://fansided.com/es/leagues/nba",
    #     'Beisbol': "https://fansided.com/es/leagues/mlb"
    # }


    # for sport, url in urls.items():

    #     web_scrapper = FansidedScrapper(url, news_source, sport)
    #     html = web_scrapper.fetch_html()
    #     arr = web_scrapper.analyze_html(html)
    #     if arr.empty:
    #         raise ValueError("No news collected")
    #     news_df= pd.concat([arr, news_df], ignore_index=True)

    # ##Espn
    # news_source = "Espn"
    # urls = {
    #     'Futbol': "https://www.espn.com.mx/futbol/",
    #     'Basquetbol': "https://www.espn.com.mx/basquetbol/",
    #     'Beisbol': "https://www.espn.com.mx/beisbol/"
    # }


    # for sport, url in urls.items():

    #     web_scrapper = EspnScrapper(url, news_source, sport)
    #     html = web_scrapper.fetch_html()
    #     arr = web_scrapper.analyze_html(html)
    #     if arr.empty:
    #         raise ValueError("No news collected")
    #     news_df= pd.concat([arr, news_df], ignore_index=True)

    json_data = news_df.to_json()


    # * Insert the json dataframe into s3 bucket
    def insert_to_s3(key):

        client = boto3.client('s3')

        client.put_object(
            Bucket='automatizacion-uni-2024',
            Key= key,
            Body=json_data
        )

    def insert_to_dynamo(file):
        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('Automatizacion-discord-dataset')

        table.put_item(
            Item={
                #Round about para que me funcione la cagada de DynamoDb
                'dataset_id': '1',
                'created_at': str(datetime.now()),
                'file_name': file,
            }
        )

    file_name = 'dataframe_noticias_' + str(datetime.now()) + '.json'
    insert_to_s3(file_name)
    insert_to_dynamo(file_name)
    print("Execution succcessfully completed")

lambda_handler('dfj','dfds')
