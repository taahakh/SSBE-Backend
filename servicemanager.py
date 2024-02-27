import json
# from other import summarise , SummarisationManager
from other import SummarisationManager
from bs4 import BeautifulSoup

class ServiceManager:

    def __init__(self):
        self.summ = SummarisationManager()
        self.placeholder_text = """
        Ancient Egyptian literature was written with the Egyptian language from ancient Egypt's pharaonic period until the end of Roman domination. It represents the oldest corpus of Egyptian literature. Along with Sumerian literature, it is considered the world's earliest literature.[1]
        """

    def get_sum_customisation(self, location):
        with open(location, 'r') as file:
            return json.load(file)

    def start_summarisation(self, data):
        # print(self.summ.summarise(self.placeholder_text, 'BartXIV'))
        # print(self.summ.summarise(self.placeholder_text, 'BartLargeCNN'))
        # return 'yes'
        return data["text"]
        # print(data)
        # DISABLED ACTUAL SUMMARISATION
        # return self.summ.summarise(data["text"], data['customisation']['model'])
        # self.summ.summarise(self.placeholder_text, 'T5MedicalSummarisation')

    
    def start_scraping(self, data):
        print("Scraping")
        soup = BeautifulSoup(data["text"], 'html.parser')
        # print(soup.find_all('h1'))
        [s.extract() for s in soup(['style', 'script', 'link', 'footer', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        print(visible_text)
        return json.dumps({"data": visible_text})
