from web_scraper import WebScraper
from bs4 import BeautifulSoup
import pandas as pd

class EspnScrapper(WebScraper):

    def analyze_html(self, html):

        soup = BeautifulSoup(html.content, 'html.parser')

        noticias = []
        section = soup.find(attrs={'id':'news-feed'})

        if(self.sport == 'Basquetbol'):
            for row in section.find_all('article'):
                content_item = row.find(class_='contentItem__titleWrapper')
                if(
                    content_item is not None
                    and (content_item.find('h2') is not None)
                    and (content_item.find('p') is not None)
                    and (row.find('source') is not None)
                ):
                    title = content_item.find('h2').get_text()
                    description =  content_item.find('p').get_text()
                    image = row.find('source')['data-srcset']
                    link = "https://www.espn.com.mx" + row.find('a')['href']
                    # print(image)
                    noticias.append([title,description, image, link, self.news_source, self.sport])

        else:
            for row in section.find('section').find_all('section'):

                content_item = row.find(class_='contentItem__titleWrapper')
                if(
                    content_item is not None
                    and (content_item.find('h2') is not None)
                    and (content_item.find('p') is not None)
                    and (row.find('img') is not None)
                ):
                    title = content_item.find('h2').get_text()
                    description =  content_item.find('p').get_text()
                    image = row.find('img')['data-default-src']
                    link = "https://www.espn.com.mx" + row.find('a')['href']

                    noticias.append([title,description, image, link, self.news_source, self.sport])


        df = pd.DataFrame(noticias, columns=['title', 'description',  'image', 'link','news source', 'sport'])
        return df

# urls = {
#     # 'Futbol': "https://www.espn.com.mx/futbol/",
#     'Basquetbol': "https://www.espn.com.mx/basquetbol/",
#     # 'Beisbol': "https://www.espn.com.mx/beisbol/"
# }

# news_source = "Espn"

# for sport, url in urls.items():

#     web_scrapper = EspnScrapper(url, news_source, sport)
#     html = web_scrapper.fetch_html()
#     arr = web_scrapper.analyze_html(html)
#     print(arr)

