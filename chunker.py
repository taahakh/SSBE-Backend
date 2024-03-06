class ChunkedSummarizer:
    def __init__(self, t, m, max_chunk_length=512, min_summary_length=100, max_summary_length=500):
        self.tokenizer = t
        self.model = m
        self.max_chunk_length = max_chunk_length # max token length for the chunk
        self.min_summary_length = min_summary_length # min token length for the summary
        self.max_summary_length = max_summary_length # max token length for the summary

    # Can be overriden
    def tokenize_input(self, input_text):
        return self.tokenizer(input_text, return_tensors="pt", truncation=True)

    # Can be overriden
    def model_generate(self, input_ids):
        return self.model.generate(input_ids, min_length=self.min_summary_length, max_length=self.max_summary_length, num_beams=4, early_stopping=True)
    
    # Can be overriden
    def decode_summary(self, summary_ids):
        return self.tokenizer.decode(summary_ids, skip_special_tokens=True)

    #SHOULD NOT BE OVERRIDEN
    def summarize_chunked_text(self, input_text):
        # Tokenise the entire input text
        tokenized_input = self.tokenize_input(input_text)

        # Tokenised input sequence length
        input_sequence_length = tokenized_input["input_ids"].shape[1]

        # Current position of the chunk of tokenised input
        current_position = 0

        # Concatenated summary of all the chunks
        aggregated_summary = ""

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
        
        print(aggregated_summary)
        print(f'Total Chunks: {current_position/self.max_chunk_length}')
        return aggregated_summary.strip()

