class ChunkedSummarizer:
    def __init__(self, t, m, max_chunk_length=512, max_summary_length=150):
        self.tokenizer = t
        self.model = m
        self.max_chunk_length = max_chunk_length
        self.max_summary_length = max_summary_length

    def summarize_chunked_text(self, input_text):
        # Tokenize the entire input text
        tokenized_input = self.tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)

        # Get the tokenized input sequence length
        input_sequence_length = tokenized_input["input_ids"].shape[1]

        # Initialize variables to keep track of the current position and summary
        current_position = 0
        aggregated_summary = ""

        while current_position < input_sequence_length:
            # Determine the start and end positions for the current chunk
            start_position = current_position
            end_position = min(current_position + self.max_chunk_length, input_sequence_length)

            # Extract the current chunk from the tokenized input
            chunked_input = {key: value[:, start_position:end_position] for key, value in tokenized_input.items()}

            # Generate summary for the current chunk
            summary_ids = self.model.generate(chunked_input["input_ids"], min_length=100, max_length=self.max_summary_length, num_beams=4, early_stopping=True)

            # Decode the summary for the current chunk
            chunk_summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

            # Append the summary for the current chunk to the aggregated summary
            aggregated_summary += chunk_summary + "\n\n"

            # Move the current position to the next chunk
            current_position += self.max_chunk_length
        
        print(aggregated_summary)
        return aggregated_summary.strip()

# Example usage
# chunked_summarizer = ChunkedSummarizer(model_name="facebook/bart-large-cnn", max_chunk_length=512, max_summary_length=150)
# input_text = "Your long input text goes here..."
# summary = chunked_summarizer.summarize_chunked_text(input_text)
# print("Original Text:", input_text)
# print("Aggregated Summary:", summary)
