import os
import openai
import tiktoken

import os
import openai

class OpenAI_Summarizer:
    """
    This class uses OpenAI's GPT-3 model to summarize a transcript into bullet points. It can calculate the number of tokens in the input and output text, estimate the price of generating the summary based on token usage, save the summary to a text file, and display notes if required.
    
    -----------
    Parameters:
    -----------
    
    transcript_text : str
        The input transcript that needs to be summarized.

    summarizer_model : str, optional (default="gpt-3.5-turbo")
        The OpenAI model to use for summarizing the transcript.

    USD_per_1k : float, optional (default=0.002)
        The price charged per 1,000 tokens used.

    encoding_name : str, optional (default="cl100k_base")
        The encoding type to use for encoding the input and output text.

    --------
    Methods:
    --------
    num_tokens_from_input_string() -> int:
        Calculates the number of tokens in the input text using the specified encoding and returns it.

    summarize_text(system_prompt:str, n_items:int=None, model:str="gpt-3.5-turbo", show_notes:bool=False) -> str:
        Summarizes the input text into a bulleted list of n-items using the OpenAI GPT-3 model as default, given a system prompt, and returns the summarized text.

    save_txt(export_dir):
        Saves the summarized text to a text file with the specified export directory.

    get_price() -> dict:
        Calculates the price for generating the summarized text based on the number of tokens used, and returns it as a dictionary.

    num_tokens_from_output_string(encoding_name:str="cl100k_base") -> int:
        Calculates the number of tokens from the output string.
    
    -----------
    Attributes:
    -----------
    
    transcript_text : str
        The input transcript that needs to be summarized.

    summarizer_model : str
        The OpenAI model to use for summarizing the transcript.

    USD_per_1k : float
        The price charged per 1,000 tokens used.

    encoding_name : str
        The encoding type to use for encoding the input and output text.

    input_encoding : tiktok.Encoding
        The encoding used to encode the input text.

    input_num_tokens : int
        The number of tokens in the input text.

    response : openai.api_models.ModelAPIResponse
        The response object returned by the OpenAI API after generating the summarized text.

    summarized_text : str
        The summarized text in bullet-point form.

    output_usage_dict : dict
        A dictionary containing the token usage of the OpenAI API after generating the summarized text.

    output_tokens_count : int
        The total number of tokens used by the OpenAI API after generating the summarized text.

    output_price_dict : dict
        A dictionary containing the cost of generating the summarized text based on token usage.

    ---------
    Examples:
    ---------
    
    # Create an instance of the OpenAI_Summarizer class
    summarizer = OpenAI_Summarizer(transcript_text="This is an example transcript.")

    # Calculate the number of input tokens
    num_input_tokens = summarizer.num_tokens_from_input_string()
    
    # Define role_txt for system_prompt
    role_txt = "'You are a graduating SHS student, excellent at summarizing notes in layman's terms."

    # Summarize the transcript into 3 bullet points
    summarized_text = summarizer.summarize_text(system_prompt=role_txt, n_items=3)

    # Save the summarized text to a text file
    summarizer.save_txt(export_dir="example_summarized_text")

    # Calculate the cost of generating the summary
    output_price = summarizer.get_price()

    # Calculate the number of output tokens
    num_output_tokens = summarizer.num_tokens_from_output_string()
    """
    def __init__(self, 
                 transcript_text:str, 
                 summarizer_model:str = "gpt-3.5-turbo", 
                 USD_per_1k:float = 0.002, 
                 encoding_name:str = "cl100k_base"):
        """
        Initializes the instance of the OpenAI_Summarizer class with the input text, model, USD_per_1k, and encoding_name parameters.
    
        Parameters:
        -----------
        transcript_text : str
            The input text to be summarized.
        summarizer_model : str, optional
            The name of the OpenAI language model to be used for summarization. Default is "gpt-3.5-turbo".
        USD_per_1k : float, optional
            The cost of 1000 tokens in USD. Default is 0.002.
        encoding_name : str, optional
            The name of the encoding to be used for tokenization. Default is "cl100k_base".

        Returns:
        --------
        None

        """
        self.transcript_text = transcript_text
        self.summarizer_model = summarizer_model
        self.USD_per_1k = USD_per_1k
        self.encoding_name = encoding_name
        
    def num_tokens_from_input_string(self) -> int:
    
        """
        Calculates the number of tokens in the input text using the specified encoding and returns it.

        Returns:
            An integer representing the number of tokens in the input text.
        """
    
        self.input_encoding = tiktoken.get_encoding(self.encoding_name)
        self.input_num_tokens = len(self.input_encoding.encode(self.transcript_text))

    def summarize_text(self, 
                       system_prompt:str, 
                       n_items:int = None, 
                       model:str = "gpt-3.5-turbo", 
                       show_notes:bool=False) -> str:
        """
        Summarizes the input text into a bulleted list of n-items using the OpenAI GPT-3 model as default, 
        given a system prompt, and returns the summarized text.

        Parameters:
        -----------
        system_prompt: str
            A prompt to be fed into the OpenAI API model.
        
        n_items: int
            The number of bullet points the summarized text should contain.
        
        model: str
            The OpenAI API model to use for the text summarization.
        
        show_notes: bool
            If True, it prints the summarized text.

        Returns:
        --------
        str
            The summarized text.

        Prints:
        -------
        If show_notes=True, it prints the summarized text.

        Exceptions:
        -----------
        Raises an OpenAI API Exception if there is an issue with the OpenAI API authentication.
        """
        self.response = openai.ChatCompletion.create(
            model=self.summarizer_model,
            messages=[
                {"role":"system", 
                 "content": system_prompt},
                
                {"role":"user", 
                 "content": f"Summarize the following transcript into {n_items} key bullet points: '\n{self.transcript_text}'"}
            ])

        self.summarized_text = self.response['choices'][0]['message']['content']
        self.output_usage_dict = dict(self.response['usage'])
        self.output_tokens_count = self.output_usage_dict['total_tokens']

        if show_notes==True:
            print(self.summarized_text)
    
    def save_txt(self, export_dir): 
        """
        Saves the summarized text to a text file with the specified export directory.
        
        Parameters:
        -----------
        export_dir : str
            The directory path where the summarized text will be saved as a .txt file.
        
        Returns:
        --------
        None
        
        Prints:
        -------
        A message indicating where the summarized note was saved.
        """
        with open(f"{export_dir}.txt", 'w', encoding="utf-8") as f:
            f.write(self.summarized_text)
            f.close()
            
        print(f"Summarized note saved at: {export_dir}.txt")
        

    def get_price(self) -> dict: 
        """
        Calculates the price for generating the summarized text based on the number of tokens used, and returns it as a dictionary.
        
        Parameters:
        None
        
        Returns:
        output_price_dict (dict): a dictionary containing the cost of generating the summarized text based on the number of tokens used.
        
        Prints:
        None
        
        Raises:
        None
        """
        self.output_price_dict = {k: v*(self.USD_per_1k/1000.0) for (k, v) in self.output_usage_dict.items()}

    
    def num_tokens_from_output_string(self, 
                                      encoding_name:str = "cl100k_base") -> int:
        """
        Calculates the number of tokens in the output string using the specified encoding and returns it.
        
        Parameters:
        -----------
        encoding_name: str
            The name of the encoding to use in the tokenization process.
            Default is 'cl100k_base'.
            
        Returns:
        --------
        output_num_tokens: int
            The number of tokens in the summarized output text.
            
        Raises:
        -------
        None
        """
        self.output_encoding = tiktoken.get_encoding(self.encoding_name)
        self.output_num_tokens = len(self.output_encoding.encode(self.summarized_text))