from model_interface import ModelInterface, SummaryType, TextType
# from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from chunker import ChunkedSummarizer

# Model link https://huggingface.co/facebook/bart-large-cnn
class Model(ModelInterface):

    def __init__(self):
        self.tokenizer = None
        self.model = None

    @property
    def minimum_summary_length(self) -> int:
        return 60

    @property
    def maximum_summary_length(self) -> int:
        return 512

    # Abstractive (ab) / Extractive (ex)
    @property
    def summary_type(self) -> SummaryType:
        return SummaryType.ABSTRACTIVE
    
    @property
    def text_type(self) -> list[TextType]:
        return [TextType.GENERAL, TextType.NEWS, TextType.FINANCIAL, TextType.MEDICAL, TextType.SCIENTIFIC]
    
    @property
    def defined_tokenizer(self):
        return self.tokenizer
    
    @property
    def defined_model(self):
        return self.model

    # Little description about the model
    @property
    def description(self) -> str:
        return "Good for all types of text"

    @property
    def model_name(self):
        return 'BartLargeCNN'

    def load_model(self):
        if self.model is None:
            print("(BartLargeCNN) Loading model...")
            # self.pipe = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
            self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
            print(len(self.tokenizer))
            self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")
            print("(BartLargeCNN) Model loaded")

    def unload_model(self):
        print("(BartLargeCNN) Unloading model...")
        self.tokenizer = None
        self.model = None
        print("(BartLargeCNN) Model unloaded")

    @ModelInterface.catch_exception
    def summarise(self, text, summary_length):
        print("(BartLargeCNN) Summarising...")
        # print(summary_length)
        length = self.maximum_summary_length
        # print(summary_length, length)
        # if summary_length != "":
        #     length = int(summary_length)
        # print(summary_length, length)
        chunked_summarizer = ChunkedSummarizer(t=self.tokenizer, m=self.model, max_chunk_length=512, max_summary_length=length)
        return chunked_summarizer.summarize_chunked_text(text)
