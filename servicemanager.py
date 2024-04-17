import json
from summarisationmanager import SummarisationManager
from summarizer.bert import Summarizer #  BERT Summariser for text reduction
from boilerpy3 import extractors # HTML content extraction

class ServiceManager:

    def __init__(self):
        """
        Initialise ServiceManager.

        Initialise SummarisationManager and BERT Summariser.
        """
        self.summ = SummarisationManager()
        self.reductor_model = Summarizer()

    def get_sum_customisation(self, location):
        """
        Get summarisation customisation from JSON file.

        Args:
            location (str): Location of the JSON file.

        Returns:
            dict: Summarisation customisation.
        """
        with open(location, 'r') as file:
            return json.load(file)
    
    # CHANGE NAME - also in test file
    def fix_escape_chars(self, text):
        """
        Removes literal / non-literal escape characters (newlines, tabs) and quotes.

        Args:
            text (str): Input text.

        Returns:
            str: Text with escaped / other characters replaced.
        """
        return text.replace('\\n', '').replace('\n', '').replace('\\t', '').replace('\t', '').replace('\\"', '"')
    
    def reductor(self, text, r=0.5):
        """
        Reduces the given text using the reductor (BERT Extractive) model.

        Parameters:
        - text (str): The text to be reduced.
        - r (float): The reduction ratio. Default is 0.5.

        Returns:
        - str: The reduced text.
        """
        result = self.reductor_model(text, ratio=r)
        return ''.join(result)
    
    def start_summarisation(self, data):
        """
        Start the summarisation process. Handles html and non-html content and manages different piplines for abstractive / extractive summaries.

        Args:
            data (dict): A dictionary containing the input data for summarisation.

        Returns:
            tuple: A tuple containing the summarisation state and the generated summary content.
                The summarisation state is a boolean indicating whether the summarisation was successful.
                The generated summary content is a string containing the summarised text.

        Raises:
            None

        """
        content = data["text"]

        # if extractedType == "extracted" or anything else,
        # then skip this code block
        if (data['extractedType'] == 'html'):
            # Extract content from HTML
            extractor = extractors.ArticleExtractor()
            try:
                content = extractor.get_content(content)
            except:
                # Document is not proper html
                print('Error extracting html content')
                return False, None

        content = self.fix_escape_chars(content)

        # Setting up the summary length
        # If no summary length is provided, format l as an empty string indicating no summary length
        # If summary length is provided, check if it is a valid number between 0 and 100; normalise between 0 - 1; convert it to a float
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

        # Reducing the content
        content = self.reductor(content)

        # Summarising the content
        state, content = self.summ.summarise(content, data['customisation']['model'], l)

        # If summarisation failed, return state and None
        if not state:
            return state, None

        # If summarisation was successful and the model is abstractive, reduce the content if a summary length was provided
        if l != "" and self.summ.is_model_abstractive(data['customisation']['model']) is not None:
            l = float(l)

            content = self.reductor(content, l)

        return state, content

