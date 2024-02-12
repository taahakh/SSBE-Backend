import json
from other import summarise
from bs4 import BeautifulSoup

class ServiceManager:
    def start_summarisation(self, data):
        return summarise(data["text"])

    def start_scraping(self, data):
        print("Scraping")
        soup = BeautifulSoup(data["text"], 'html.parser')
        # print(soup.find_all('h1'))
        [s.extract() for s in soup(['style', 'script', 'link', 'footer', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        print(visible_text)
        return json.dumps({"data": "Done"})
