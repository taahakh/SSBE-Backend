from enum import Enum
from abc import ABC, abstractmethod

class SummaryType(Enum):
    ABSTRACTIVE = "Abstractive"
    EXTRACTIVE = "Extractive"

class TextType(Enum):
    GENERAL = "General"
    NEWS = "News"
    FINANCIAL = "News"
    MEDICAL = "Medical"
    SCIENTIFIC = "Scientific"

class ModelInterface(ABC):

    def catch_exception(func):
        def wrapper(self, text, summary_length):
            try:
                return True, func(self, text, summary_length)
            except (Exception, RuntimeError) as e:
                print("An exception occurred: ", e)
                self.unload_model();
                return False, None
        return wrapper

    @property
    @abstractmethod
    def minimum_summary_length(self) -> int:
        pass

    @property
    @abstractmethod
    def maximum_summary_length(self) -> int:
        pass

    # Abstractive (ab) / Extractive (ex)
    @property
    @abstractmethod
    def summary_type(self) -> SummaryType:
        return
    
    @property
    @abstractmethod
    def text_type(self) -> list[TextType]:
        return

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    # Little description about the model
    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def load_model(self) -> None:
        pass

    @abstractmethod
    @catch_exception
    def summarise(self, text, summary_length) -> str:
        pass

    @abstractmethod
    def unload_model(self) -> None:
        pass


