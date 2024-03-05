import json
# from other import summarise , SummarisationManager
from other import SummarisationManager
from bs4 import BeautifulSoup
from summarizer.bert import Summarizer # help reduce the size of the text for the actual model (extraction)
# import justext
from boilerpy3 import extractors
# import re
# from summa.summarizer import summarize

class ServiceManager:

    def __init__(self):
        self.summ = SummarisationManager()
        # self.placeholder_text = """
        # Ancient Egyptian literature was written with the Egyptian language from ancient Egypt's pharaonic period until the end of Roman domination. It represents the oldest corpus of Egyptian literature. Along with Sumerian literature, it is considered the world's earliest literature.[1]
        # """

    def get_sum_customisation(self, location):
        with open(location, 'r') as file:
            return json.load(file)
    
    def fix_escape_chars(self, text):
        return text.replace('\\n', '').replace('\n', '').replace('\\t', '').replace('\t', '').replace('\\"', '"')

    def start_summarisation(self, data):
        content = data["text"]
        print('extractedType: ', data['extractedType'])
        # print('Text: ', txt)

        if (data['extractedType'] == 'html'):
            print('HTML')
            extractor = extractors.ArticleExtractor()

            content = extractor.get_content(content)
            content = self.fix_escape_chars(content)

            print('Content: ', content)

        # ok = summarize(content, ratio=0.5)

        print("\n-------------------\n")
      
        model = Summarizer()
        result = model(content, ratio=0.8)
        full = ''.join(result)
        print('Text reducer: ', full)
        # # return full
        # print(data)

        # print('Text: ', ok)


        # paragraphs = justext.justext(content, justext.get_stoplist("English"))
        # for paragraph in paragraphs:
        #     if not paragraph.is_boilerplate:
        #         print(paragraph.text)

        # return data
        # return txt
        # return full
        return self.summ.summarise(full, data['customisation']['model'])
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
