# Main - WebServer and API

## API

### LoginResource
Login to the application
    
    Endpoint: POST /auth/login

#### Request Body
    {
        "username": "",
        "password": ""
    }

#### Response Body
    {
        "message": "Login/Connect Successful",
        "api_key": ...,
        "state": "GOOD"
    }

### SignupResource
User signup for the application
    
    Endpoint: POST /auth/signup

#### Request Body
    {
        "username": "",
        "password": ""
    }

#### Response Body
    {
        "message": "Signup Successful!",
        "api_key": ...,
        "state": "GOOD"
    }

### JsonFileResource
User signup for the application
    
    Endpoint: GET /auth/signup

#### Response Body
    {
        "data": "Signup Successful!"
    }

### ServiceManagerResource
Resource Endpoint for the summarisation pipeline
    
    Endpoint: POST /servicemanager/summarise

#### Request Body
    {
        "text": "...",
        "customisation": {
            "summary-length": 50,
            "model": BartLargeCNN
        },
        extractedType: "html"
    }

text: string \
customisation --> summary-length: int, range 0-100 \
extractedType: string, [html, extracted]

#### Response Body
    {
        "status": "success",
        "data": "...."
    }

# Database Models
User

# ServiceManager
## get_sum_customisation(self, location)
    
 Get summarisation customisation from JSON file.

    Args:
        location (str): Location of the JSON file.

    Returns:
        dict: Summarisation customisation.
    
## fix_escape_chars(self, text)
Removes literal / non-literal escape characters (newlines, tabs) and quotes.

    Args:
        text (str): Input text.

    Returns:
        str: Text with escaped / other characters replaced.

## reductor(self, text, r=0.5)
Reduces the given text using BERT extractive model.

    Parameters:
    - text (str): The text to be reduced.
    - r (float): The reduction ratio. Default is 0.5.

    Returns:
    - str: The reduced text.


## start_summarisation(self, data)
Start the summarisation process. Handles html and non-html content and manages different piplines for abstractive / extractive summaries.

        Args:
            data (dict): A dictionary containing the input data for summarisation.

        Returns:
            tuple: A tuple containing the summarisation state and the generated summary content.
                The summarisation state is a boolean indicating whether the summarisation was successful.
                The generated summary content is a string containing the summarised text.

        Raises:
            None

# SummarisationManager
## __init__(self, model_src_path='model_list.txt', json_output_path='md.json')

        Initialises a SummarisationManager object. Stores a list of models and creates a JSON file containing model descriptors.

        Args:
            model_src_path (str): The path to the model source file. Defaults to 'model_list.txt'.
            json_output_path (str): The path to the JSON output file. Defaults to 'md.json'.

## create_model_descriptors(self, output_path)

        Creates model descriptors for each model, inherited with abstract base class ModelInterface, in the model list and saves them to a JSON file.

        Args:
            output_path (str): The path to the output JSON file.

        Returns:
            None

## load_resources(self, src_path) -> bool

        Loads specified models from the specified source path.

        Args:
            src_path (str): The path to the file containing the list of models.

        Returns:
            bool: True if the resources are successfully loaded, False otherwise.

## model_loader(self, model)
        Loads the specified model and sets it as the current loaded model.

        Args:
            model (str): The name of the model to load.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the model was loaded successfully,
                   and the loaded model object if successful, or None if unsuccessful.

## is_model_abstractive(self, model_name)
        Checks if a given model is abstractive.

        Parameters:
        - model_name (str): The name of the model to check.

        Returns:
        - Model: The abstractive model if it exists, otherwise None.

## summarise(self, text, model_name, summary_length)
        Summarizes the given text using the specified model and summary length.

        Args:
            text (str): The text to be summarized.
            model_name (str): The name of the model to be used for summarization.
            summary_length (int): The desired length of the summary.

        Returns:
            tuple: A tuple containing a boolean value indicating whether the model was found,
                   and the summarized text if the model was found, otherwise None.

# SummaryType - ENUM
    Enum representing the type of summary.

    Attributes:
        ABSTRACTIVE (str): Represents an abstractive summary.
        EXTRACTIVE (str): Represents an extractive summary.

# TextType - ENUM
    Enum representing different types of text.

    Attributes:
        GENERAL (str): General text type.
        NEWS (str): News text type.
        FINANCIAL (str): Financial text type.
        MEDICAL (str): Medical text type.
        SCIENTIFIC (str): Scientific text type.

# ModelInterface - AbstractBaseClass
Abstract base class for model interfaces.

## catch_exception(func)
Decorator to catch and handle exceptions when calling the summarise method

## minimum_summary_length(self) -> int
    @property
    @abstractmethod

    Get the minimum length of the summary.

## maximum_summary_length(self) -> int
    @property
    @abstractmethod
    
    Get the maximum length of the summary.

## summary_type(self) -> SummaryType
    @property
    @abstractmethod
    
    Get the type of summary (abstractive or extractive).

## text_type(self) -> list[TextType]
    @property
    @abstractmethod
    
    Get the supported types of input text.

## model_name(self) -> str
    @property
    @abstractmethod
    
    Get the name of the model.

## description(self) -> str
    @property
    @abstractmethod
    
    Get a brief description of the model.

## load_model(self) -> None
    @property
    @abstractmethod
    
    Load the model.

## summarise(self, text, summary_length) -> str
    @abstractmethod
    @catch_exception

    Summarize the given text.

    Args:
        text (str): The input text to be summarized.
        summary_length (int/float): The desired length of the summary.

    Returns:
        str: The generated summary.

## unload_model(self) -> None
    Unload the model.

# ChunkedSummariser
Class for summarizing large text by dividing it into chunks.
## __init__(self, t, m, max_chunk_length=512, min_summary_length=100, max_summary_length=500)
        Initialize ChunkedSummarizer.

        Args:
            t: tokeniser for tokenizing the input text.
            m: Model for generating summaries.
            max_chunk_length (int): Maximum token length for each chunk.
            min_summary_length (int): Minimum token length for the summary.
            max_summary_length (int): Maximum token length for the summary.

## tokenize_input(self, input_text)
            Tokenises the input text using the tokeniser.

            Args:
                input_text (str): The input text to be tokenised.

            Returns:
                dict: A dictionary containing the tokenised input text.

## model_generate(self, input_ids)
        Generates a summary using the underlying model.

        Args:
            input_ids (list): The input token IDs.

        Returns:
            list: The generated summary token IDs.

## decode_summary(self, summary_ids)
            Decodes the summary IDs into a human-readable summary.

            Args:
                summary_ids (list): A list of summary IDs.

            Returns:
                str: The decoded summary.

## summarize_chunked_text(self, input_text)
        Summarises the input text by chunking it into smaller parts and generating summaries for each chunk.

        Args:
            input_text (str): The input text to be summarized.

        Returns:
            str: The aggregated summary of all the chunks.

