import json
from other import SummarisationManager
from bs4 import BeautifulSoup
from summarizer.bert import Summarizer # help reduce the size of the text for the actual model (extraction)
from boilerpy3 import extractors

class ServiceManager:

    def __init__(self):
        self.summ = SummarisationManager()

    def get_sum_customisation(self, location):
        with open(location, 'r') as file:
            return json.load(file)
    
    def fix_escape_chars(self, text):
        return text.replace('\\n', '').replace('\n', '').replace('\\t', '').replace('\t', '').replace('\\"', '"')
    
    def start_summarisation(self, data):
        content = data["text"]
        print('extractedType: ', data['extractedType'])
        print(data['customisation']['summary-length'])

        if (data['extractedType'] == 'html'):
            print('HTML')
            extractor = extractors.ArticleExtractor()
            content = extractor.get_content(content)

        content = self.fix_escape_chars(content)


        print("\n-------------------\n")
      
        l = data['customisation']['summary-length']

        model = Summarizer()
        result = model(content, ratio=0.5)
        content = ''.join(result)
        print('Text reducer: ', content)

        content = self.summ.summarise(content, data['customisation']['model'], l)

        if l != "" and self.summ.is_model_abstractive(data['customisation']['model']):
            l = float(l)
            model = Summarizer()
            result = model(content, ratio=l)
            content = ''.join(result)
            print('Text reducer: ', content)

        return content

    
    # def start_scraping(self, data):
    #     print("Scraping")
    #     soup = BeautifulSoup(data["text"], 'html.parser')
    #     # print(soup.find_all('h1'))
    #     [s.extract() for s in soup(['style', 'script', 'link', 'footer', '[document]', 'head', 'title'])]
    #     visible_text = soup.getText()
    #     print(visible_text)
    #     return json.dumps({"data": visible_text})
