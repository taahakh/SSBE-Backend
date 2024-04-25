# model_interface.py
# Abstract base class for model interfaces.
# Used to implement different summarisation models.

from enum import Enum
from abc import ABC, abstractmethod

class SummaryType(Enum):
    """
    Enum representing the type of summary.

    Attributes:
        ABSTRACTIVE (str): Represents an abstractive summary.
        EXTRACTIVE (str): Represents an extractive summary.
    """
    ABSTRACTIVE = "Abstractive"
    EXTRACTIVE = "Extractive"

class TextType(Enum):
    """
    Enum representing different types of text.

    Attributes:
        GENERAL (str): General text type.
        NEWS (str): News text type.
        FINANCIAL (str): Financial text type.
        MEDICAL (str): Medical text type.
        SCIENTIFIC (str): Scientific text type.
    """
    GENERAL = "General"
    NEWS = "News"
    FINANCIAL = "Financial"
    MEDICAL = "Medical"
    SCIENTIFIC = "Scientific"

class ModelInterface(ABC):
    """
    Abstract base class for model interfaces.
    """

    # Decorator to catch and handle exceptions when calling the summarise method
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
        """
        Get the minimum length of the summary.
        """
        pass

    @property
    @abstractmethod
    def maximum_summary_length(self) -> int:
        """
        Get the maximum length of the summary.
        """
        pass

    @property
    @abstractmethod
    def summary_type(self) -> SummaryType:
        """
        Get the type of summary (abstractive or extractive).
        """
        return
    
    @property
    @abstractmethod
    def text_type(self) -> list[TextType]:
        """
        Get the supported types of input text.
        """
        return

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Get the name of the model.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Get a brief description of the model.
        """
        pass

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the model.
        """
        pass

    @abstractmethod
    @catch_exception
    def summarise(self, text, summary_length) -> str:
        """
        Summarize the given text.

        Args:
            text (str): The input text to be summarized.
            summary_length (int/float): The desired length of the summary.

        Returns:
            str: The generated summary.
        """
        pass

    @abstractmethod
    def unload_model(self) -> None:
        """
        Unload the model.
        """
        pass


