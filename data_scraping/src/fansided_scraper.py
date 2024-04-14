from web_scraper import WebScraper
from bs4 import BeautifulSoup
import pandas as pd

class FansidedScrapper(WebScraper):

    def analyze_html(self, html):

        soup = BeautifulSoup(html.content, 'html.parser')

        noticias = []
        section = soup.find(class_='wrapper_5qxxt1-o_O-padding_73yipz')
        for row in section.find_all('article'):
            # print( content_item.prettify())

            if(
                row is not None
                and row.find('h3') is not None
                and row.find('img') is not None
                and row.find('figure') is not None
               ):
                title = row.find('h3').get_text()
                description =  row.find('img')['alt']
                image = row.find('figure')
                img2 = image.find_all('img')[-1]['src']
                link = row.find('a')['href']
                # print(link)
                noticias.append([title,description, img2, link, self.news_source, self.sport])

        df = pd.DataFrame(noticias, columns=['title', 'description', 'link', 'image','news source', 'sport'])
        return df

# urls = {
#     'Futbol': "https://fansided.com/es/leagues/futbol",
#     'Basquetbol': "https://fansided.com/es/leagues/nba",
#     'Beisbol': "https://fansided.com/es/leagues/mlb"
# }

# news_source = "Fansided"

# for sport, url in urls.items():

#     web_scrapper = FansidedScrapper(url, news_source, sport)
#     html = web_scrapper.fetch_html()
#     arr = web_scrapper.analyze_html(html)
#     print('arr: ', arr)


