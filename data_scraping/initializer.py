### AS
from as_scraper import AsScrapper
from espn_scraper import EspnScrapper
from fansided_scraper import FansidedScrapper
from datetime import datetime
import pandas as pd
import boto3

def lambda_handler(event, context):

    news_df = pd.DataFrame(columns=['title', 'description', 'link', 'image','news source', 'sport'])

    print(news_df)

    ###As
    news_source = "As"
    urls = {
        'Futbol': "https://mexico.as.com/futbol/?omnil=mpal",
        'Basquetbol': "https://mexico.as.com/noticias/nba/",
        'Beisbol': "https://mexico.as.com/noticias/beisbol"
    }


    for sport, url in urls.items():

        web_scrapper = AsScrapper(url, news_source, sport)
        html = web_scrapper.fetch_html()
        arr = web_scrapper.analyze_html(html)
        news_df= pd.concat([arr, news_df], ignore_index=True)

    # ## Fansided
    # news_source = "Fansided"

    # urls = {
    #     'Futbol': "https://fansided.com/es/leagues/futbol",
    #     'Basquetbol': "https://fansided.com/es/leagues/nba",
    #     'Beisbol': "https://fansided.com/es/leagues/mlb"
    # }


    # for sport, url in urls.items():

    #     web_scrapper = FansidedScrapper(url, news_source, sport)
    #     html = web_scrapper.fetch_html()
    #     arr = web_scrapper.analyze_html(html)
    #     print('arr: ', arr)

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
    #     print(arr)

    json_data = news_df.to_json()

    # Save JSON data to a file

    # Upload JSON String to an S3 Object
    client = boto3.client('s3')

    client.put_object(
        Bucket='automatizacion-uni-2024',
        Key= 'dataframe_noticias_' + str(datetime.now()) + '.json',
        Body=json_data
    )
    print(news_df)
