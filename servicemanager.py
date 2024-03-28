import json
from other import SummarisationManager
# from bs4 import BeautifulSoup
from summarizer.bert import Summarizer # help reduce the size of the text for the actual model (extraction)
from boilerpy3 import extractors

class ServiceManager:

    def __init__(self):
        self.summ = SummarisationManager()
        self.reductor_model = Summarizer()

    def get_sum_customisation(self, location):
        with open(location, 'r') as file:
            return json.load(file)
    
    def fix_escape_chars(self, text):
        return text.replace('\\n', '').replace('\n', '').replace('\\t', '').replace('\t', '').replace('\\"', '"')
    
    def reductor(self, text, r=0.5):
        result = self.reductor_model(text, ratio=r)
        return ''.join(result)
    
    def start_summarisation(self, data):
        content = data["text"]
        print('extractedType: ', data['extractedType'])
        # print(data['customisation']['summary-length'])

        print(data)
        # if extractedType == "extracted" or anything else,
        # then skip this code block
        if (data['extractedType'] == 'html'):
            print('HTML')
            extractor = extractors.ArticleExtractor()
            try:
                content = extractor.get_content(content)
            except:
                print('Error extracting html content')
                return False, None

        content = self.fix_escape_chars(content)


        print("\n-------------------\n")
      
        if 'summary-length' not in data['customisation']:
            l = ""
        else: 
            if data['customisation']['summary-length'] == "":
                l = ""
            else:
                l = data['customisation']['summary-length']
                l = int(l)
                if l < 0 or l > 100:
                    print('Invalid summary length')
                    return False, None
                
                l = float(l/100)

        # model = Summarizer()
        # result = model(content, ratio=0.5)
        # content = ''.join(result)
        # print('Text reducer: ', content)
        print("before text reducer: ", content)
        content = self.reductor(content)
        print('Text reducer: ', content)

        state, content = self.summ.summarise(content, data['customisation']['model'], l)

        if not state:
            return state, None

        if l != "" and self.summ.is_model_abstractive(data['customisation']['model']) is not None:
            l = float(l)
            # model = Summarizer()
            # result = model(content, ratio=l)
            # content = ''.join(result)
            content = self.reductor(content, l)
            print('Text reducer: ', content)

        return state, content

