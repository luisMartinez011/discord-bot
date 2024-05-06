from web_scraper import WebScraper
from bs4 import BeautifulSoup
import pandas as pd

class AsScrapper(WebScraper):

    def analyze_html(self, html):

        soup = BeautifulSoup(html.content, 'html.parser')

        noticias = []
        section = soup.find(class_='ss-wr')
        for row in section.find('div'):

            if(
                row is not None
                # and row.find('h3') is not None
                # and row.find('img') is not None
                # and row.find('figure') is not None
               ):
                title = row.find('article').find("h2").find("a").get_text()
                description =  row.find('img')['alt']
                image = row.find('figure').find("a").find("img")["src"]
                link = row.find('article').find("h2").find("a")['href']
                noticias.append([title,description, image, link, self.news_source, self.sport])

        df = pd.DataFrame(noticias, columns=['title', 'description',  'image','link','news source', 'sport'])
        return df

# urls = {
#     'Futbol': "https://mexico.as.com/futbol/?omnil=mpal",
#     'Basquetbol': "https://mexico.as.com/noticias/nba/",
#     'Beisbol': "https://mexico.as.com/noticias/beisbol"
# }

# news_source = "As"

# for sport, url in urls.items():

#     web_scrapper = AsScrapper(url, news_source, sport)
#     html = web_scrapper.fetch_html()
#     arr = web_scrapper.analyze_html(html)
#     print('arr: ', arr)


