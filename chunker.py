# chunker.py
# Built to break up large text into smaller chunks for models in order to fit the token limit
# Used the american spelling of "summarizer" for consistency with the transformers library

class ChunkedSummarizer:
    """
    Class for summarising large text by dividing it into chunks.
    """
    def __init__(self, t, m, max_chunk_length=512, min_summary_length=100, max_summary_length=500):
        """
        Initialize ChunkedSummarizer.

        Args:
            t: tokeniser for tokenizing the input text.
            m: Model for generating summaries.
            max_chunk_length (int): Maximum token length for each chunk.
            min_summary_length (int): Minimum token length for the summary.
            max_summary_length (int): Maximum token length for the summary.
        """
        
        self.tokeniser = t
        self.model = m
        self.max_chunk_length = max_chunk_length # max token length for the chunk
        self.min_summary_length = min_summary_length # min token length for the summary
        self.max_summary_length = max_summary_length # max token length for the summary

    # Tokenise the input text
    def tokenize_input(self, input_text):
            """
            Tokenises the input text using the tokeniser.

            Args:
                input_text (str): The input text to be tokenised.

            Returns:
                dict: A dictionary containing the tokenised input text.

            """
            return self.tokeniser(input_text, return_tensors="pt", truncation=True)

    # Generate the summary for the input text
    def model_generate(self, input_ids):
        """
        Generates a summary using the underlying model.

        Args:
            input_ids (list): The input token IDs.

        Returns:
            list: The generated summary token IDs.
        """
        return self.model.generate(input_ids, min_length=self.min_summary_length, max_length=self.max_summary_length, num_beams=4, early_stopping=True)
    
    # Decode the tokenised summary to text
    def decode_summary(self, summary_ids):
            """
            Decodes the summary IDs into a human-readable summary.

            Args:
                summary_ids (list): A list of summary IDs.

            Returns:
                str: The decoded summary.

            """
            return self.tokeniser.decode(summary_ids, skip_special_tokens=True)

    # Summarize the input text in chunks
    def summarize_chunked_text(self, input_text):
        """
        Summarises the input text by chunking it into smaller parts and generating summaries for each chunk.

        Args:
            input_text (str): The input text to be summarized.

        Returns:
            str: The aggregated summary of all the chunks.

        """
        # Tokenise the entire input text
        tokenized_input = self.tokenize_input(input_text)

        # Tokenised input sequence length
        input_sequence_length = tokenized_input["input_ids"].shape[1]

        # Current position of the chunk of tokenised input
        current_position = 0

        # Concatenated summary of all the chunks
        aggregated_summary = ""

        # Loop through the input text in chunks
        while current_position < input_sequence_length:
            print(f"Chunk: {current_position}")

            # Determine the start and end positions for the current chunk
            start_position = current_position
            end_position = min(current_position + self.max_chunk_length, input_sequence_length)

            # Extract the current chunk from the tokenised input
            chunked_input = {key: value[:, start_position:end_position] for key, value in tokenized_input.items()}

            # Generate summary for the current chunk
            summary_ids = self.model_generate(chunked_input["input_ids"])

            # Decode the summary for the current chunk
            chunk_summary = self.decode_summary(summary_ids[0])

            aggregated_summary += chunk_summary + "\n\n"

            # Move to the next chunk
            current_position += self.max_chunk_length
        
        print(f'Total Chunks: {current_position/self.max_chunk_length}')
        return aggregated_summary.strip()

