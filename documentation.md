# Backend Service
## Table of Contents
- [Backend Service](#backend-service)
  - [Table of Contents](#table-of-contents)
- [Main - WebServer and API](#main---webserver-and-api)
  - [API](#api)
    - [LoginResource](#loginresource)
      - [Request Body](#request-body)
      - [Response Body](#response-body)
    - [SignupResource](#signupresource)
      - [Request Body](#request-body-1)
      - [Response Body](#response-body-1)
    - [JsonFileResource](#jsonfileresource)
      - [Response Body](#response-body-2)
    - [ServiceManagerResource](#servicemanagerresource)
      - [Request Body](#request-body-2)
      - [Response Body](#response-body-3)
- [Database Model - User](#database-model---user)
- [ServiceManager](#servicemanager)
  - [get\_sum\_customisation(self, location)](#get_sum_customisationself-location)
  - [fix\_escape\_chars(self, text)](#fix_escape_charsself-text)
  - [reductor(self, text, r=0.5)](#reductorself-text-r05)
  - [start\_summarisation(self, data)](#start_summarisationself-data)
- [SummarisationManager](#summarisationmanager)
  - [__init__(self, model\_src\_path='model\_list.txt', json\_output\_path='md.json')](#initself-model_src_pathmodel_listtxt-json_output_pathmdjson)
  - [create\_model\_descriptors(self, output\_path)](#create_model_descriptorsself-output_path)
  - [load\_resources(self, src\_path) -\> bool](#load_resourcesself-src_path---bool)
  - [model\_loader(self, model)](#model_loaderself-model)
  - [is\_model\_abstractive(self, model\_name)](#is_model_abstractiveself-model_name)
  - [summarise(self, text, model\_name, summary\_length)](#summariseself-text-model_name-summary_length)
- [SummaryType - ENUM](#summarytype---enum)
- [TextType - ENUM](#texttype---enum)
- [ModelInterface - AbstractBaseClass](#modelinterface---abstractbaseclass)
  - [catch\_exception(func)](#catch_exceptionfunc)
  - [minimum\_summary\_length(self) -\> int](#minimum_summary_lengthself---int)
  - [maximum\_summary\_length(self) -\> int](#maximum_summary_lengthself---int)
  - [summary\_type(self) -\> SummaryType](#summary_typeself---summarytype)
  - [text\_type(self) -\> List:TextType](#text_typeself---listtexttype)
  - [model\_name(self) -\> str](#model_nameself---str)
  - [description(self) -\> str](#descriptionself---str)
  - [load\_model(self) -\> None](#load_modelself---none)
  - [summarise(self, text, summary\_length) -\> str](#summariseself-text-summary_length---str)
  - [unload\_model(self) -\> None](#unload_modelself---none)
- [ChunkedSummariser](#chunkedsummariser)
  - [__init__(self, t, m, max\_chunk\_length=512, min\_summary\_length=100, max\_summary\_length=500)](#initself-t-m-max_chunk_length512-min_summary_length100-max_summary_length500)
  - [tokenize\_input(self, input\_text)](#tokenize_inputself-input_text)
  - [model\_generate(self, input\_ids)](#model_generateself-input_ids)
  - [decode\_summary(self, summary\_ids)](#decode_summaryself-summary_ids)
  - [summarize\_chunked\_text(self, input\_text)](#summarize_chunked_textself-input_text)
- [How to add new models to the backend service](#how-to-add-new-models-to-the-backend-service)
- [Model\_list.txt](#model_listtxt)
- [md.json](#mdjson)
- [Templates folder](#templates-folder)
# Main - WebServer and API
WebServer and API for the summarisation backend service. 
Handles user authentication and summarisation requests through RESTful API.
Communicates directly with ServiceManager to handle summarisation based requests (e.g. summarise text, get model descriptors).

This component is designed so that it can be extended to handle different requests. Functionality that must occur before or after the summarisation process should be handled here or pointing to different custom components. 


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

# Database Model - User
A basic database model for user authentication. Not to be used in production but can be used locally. Implemented as simple as possible for demonstration purposes (showing that it can be used as a stepping stone for an actual online service).

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(255), unique=True, nullable=False)
        password = db.Column(db.String(255), unique=True, nullable=False)
        api_key = db.Column(db.String(36), unique=True, nullable=False)

# ServiceManager
Handles summarisation requests and customisation.

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

This component is designed to be a layer between the API and the summarisation models. Functionality that must occur before or after the summarisation process should be handled here.

        Args:
            data (dict): A dictionary containing the input data for summarisation.

        Returns:
            tuple: A tuple containing the summarisation state and the generated summary content.
                The summarisation state is a boolean indicating whether the summarisation was successful.
                The generated summary content is a string containing the summarised text.

        Raises:
            None

# SummarisationManager

Carries out summarisation, manages the resources of multiple models and creating model descriptors for use in the extension.

This component is designed to carry out summarisation using different selected models. Summarisation functionailty should be implemented in the models themselves or in this component.

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
Abstract base class for model interfaces. Used to define the interface for summarisation models. Add your own models by inheriting from this class.

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

## text_type(self) -> List:TextType
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
Class for summarising large text by dividing it into chunks.
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

# How to add new models to the backend service

1. Create a new class (within the models folder) that inherits from the `ModelInterface` abstract base class. This class must be named as "Model"
2. Implement the required methods in the new class - see the `ModelInterface` class for details
3. Add the new model to the `model_list.txt` file (the name added must match the file name of the new model class)

# Model_list.txt

This file contains the list of models that you can use for summarisation. Add or remvove implemented models as neeeded. The name of the model you want to add must match the file name.

# md.json

This file contains the model descriptors that are used by the extension. It is automatically generated by the `SummarisationManager` class. The descriptors are used to provide information about the models to the extension.

# Templates folder

This folder contains HTML templates which are used to test the summarisation service. The templates are used to display the summarised text in a user-friendly format. This is not used in production but can be used locally for testing purposes.