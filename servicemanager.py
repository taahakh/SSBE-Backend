import json
# from other import summarise , SummarisationManager
from other import SummarisationManager
from bs4 import BeautifulSoup
from summarizer import Summarizer # help reduce the size of the text for the actual model (extraction)
import justext
from boilerpy3 import extractors
import re
from summa.summarizer import summarize

class ServiceManager:

    def __init__(self):
        self.summ = SummarisationManager()
        self.placeholder_text = """
        Ancient Egyptian literature was written with the Egyptian language from ancient Egypt's pharaonic period until the end of Roman domination. It represents the oldest corpus of Egyptian literature. Along with Sumerian literature, it is considered the world's earliest literature.[1]
        """

    def get_sum_customisation(self, location):
        with open(location, 'r') as file:
            return json.load(file)
    
    def fix_escape_chars(self, text):
        return text.replace('\\n', '').replace('\n', '').replace('\\t', '').replace('\t', '').replace('\\"', '"')

    def start_summarisation(self, data):
        # print(self.summ.summarise(self.placeholder_text, 'BartXIV'))
        # print(self.summ.summarise(self.placeholder_text, 'BartLargeCNN'))
        # return 'yes'
        txt = data["text"]
        # model = Summarizer()
        # result = model(txt, min_length=60, max_length=512)
        # full = ''.join(result)
        # print(full)
        # return full
        # print(data)
        # DISABLED ACTUAL SUMMARISATION
        # full = txt

        # print('Text: ', txt)

        extractor = extractors.ArticleExtractor()

        content = extractor.get_content(txt)
        content = self.fix_escape_chars(content)

        print('Content: ', content)

        txt = summarize(content, ratio=0.2, language='english')

        print("\n-------------------\n")
        print('Text: ', txt)

        # model = Summarizer()
        # result = model(content, min_length=60, max_length=512)
        # full = ''.join(result)
        # print('Text reducer: ', full)
        # return full
        # print(data)

        # paragraphs = justext.justext(content, justext.get_stoplist("English"))
        # for paragraph in paragraphs:
        #     if not paragraph.is_boilerplate:
        #         print(paragraph.text)

        return txt
        # return self.summ.summarise(txt, data['customisation']['model'])
        # return self.summ.summarise(data["text"], data['customisation']['model'])
        # self.summ.summarise(self.placeholder_text, 'T5MedicalSummarisation')
        # return self.summ.summarise(full, data['customisation']['model'])

    
    def start_scraping(self, data):
        print("Scraping")
        soup = BeautifulSoup(data["text"], 'html.parser')
        # print(soup.find_all('h1'))
        [s.extract() for s in soup(['style', 'script', 'link', 'footer', '[document]', 'head', 'title'])]
        visible_text = soup.getText()
        print(visible_text)
        return json.dumps({"data": visible_text})
