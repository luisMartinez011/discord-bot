from web_scraper import WebScraper
from bs4 import BeautifulSoup
import pandas as pd

class EspnScrapper(WebScraper):

    def analyze_html(self, html):

        # # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(html.content, 'html.parser')

        noticias = []
        section = soup.find(attrs={'id':'news-feed'})
        for row in section.find('section').find_all('section'):

            content_item = row.find(class_='contentItem__titleWrapper')
            # print( row.prettify())

            if(
                content_item is not None
                and (content_item.find('h2') is not None)
                and (content_item.find('p') is not None)
                and (row.find('img') is not None)
               ):
                title = content_item.find('h2').get_text()
                description =  content_item.find('p').get_text()
                image = row.find('img')['data-default-src']
                noticias.append([title,description, image, self.news_source])

        df = pd.DataFrame(noticias, columns=['title', 'description', 'image','news source'])
        return df

url = "https://www.espn.com.mx/futbol/"
news_source = "Espn"
web_scrapper = EspnScrapper(url, news_source)
html = web_scrapper.fetch_html()
arr = web_scrapper.analyze_html(html)
print('arr: ', arr)
