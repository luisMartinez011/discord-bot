from botocore.vendored import requests
import time
from bs4 import BeautifulSoup

class WebScraper():

    def __init__(self, url, news_source, sport):
        self.url = url
        self.news_source = news_source
        self.sport = sport

    def fetch_html(self):
        url = self.url
        header = {'User-Agent': 'Mozilla/5.0'}

        try:

            response = requests.get(url, headers=header)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
        finally:
            time.sleep(1)

    # def analyze_html(self, html):
    #     raise NotImplementedError("Subclasses must implement analyze_html method")

    def analyze_html(self, html):
        pass

    def example():

        html = """
        <div class="top-panel">
        <div class="inside-panel-0">
        <h1 id="h1-title ohayo">
        Some Title
        </h1>
        </div>
        <div class="inside-panel-0">
        <div class="inside-panel-1">
        <p>
            I want to extract this copy
        </p>
        </div>
        <div class="inside-panel-1">
        <p>
            I want to extract this copy
        </p>
        </div>
        </div>
        </div>

        """

        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())

        p_tags = soup.find(id='h1-title ohayo')
        print(p_tags)



