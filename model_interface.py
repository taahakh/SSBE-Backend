from abc import ABC, abstractmethod

class ModelInterface(ABC):

    def catch_exception(func):
        def wrapper(self, text):
            try:
                return True, func(self, text)
            except (Exception, RuntimeError) as e:
                print("An exception occurred: ", e)
                self.unload_model();
                return False, None
        return wrapper

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    @catch_exception
    def summarise(self, text):
        pass

    @abstractmethod
    def unload_model(self):
        pass


