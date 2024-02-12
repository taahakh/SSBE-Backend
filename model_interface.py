from abc import ABC, abstractmethod

class ModelInterface(ABC):

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def summarise(self, text):
        pass
