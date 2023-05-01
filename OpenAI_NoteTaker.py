from OpenAI_Transcriber import OpenAI_Transcriber
from OpenAI_Summarizer import OpenAI_Summarizer

class OpenAI_NoteTaker(OpenAI_Transcriber, OpenAI_Summarizer):

    def __init__(self, 
                 input_dir:str, 
                 transcriber_model:str = "whisper-1", 
                 USD_per_min:float = 0.006, 
                 summarizer_model:str = "gpt-3.5-turbo", 
                 USD_per_1k:float = 0.002, 
                 encoding_name:str = "cl100k_base"):
        """
        Initializes an instance of the OpenAI_NoteTaker class.

        Args:
            input_dir (str): The path to the directory containing the audio files to be transcribed and summarized.
            transcriber_model (str, optional): The name of the OpenAI transcription model to use. Defaults to "whisper-1".
            USD_per_min (float, optional): The price per minute charged by the transcription model, in USD. Defaults to 0.006.
            summarizer_model (str, optional): The name of the OpenAI summarization model to use. Defaults to "gpt-3.5-turbo".
            USD_per_1k (float, optional): The price per 1,000 tokens charged by the summarization model, in USD. Defaults to 0.002.
            encoding_name (str, optional): The name of the character-level encoding used by the summarization model. Defaults to "cl100k_base".
        """
        super().__init__(input_dir=input_dir, 
                         transcriber_model=transcriber_model, 
                         USD_per_min=USD_per_min,  
                        )
        """
        Initializes an instance of the OpenAI_Transcriber class.

        Args:
            input_dir (str): The path to the directory containing the audio files to be transcribed.
            transcriber_model (str): The name of the OpenAI transcription model to use.
            USD_per_min (float): The price per minute charged by the transcription model, in USD.
        """
        self.summarizer_model = summarizer_model
        self.USD_per_1k = USD_per_1k
        self.encoding_name = encoding_name
        
    
    def take_notes(self, 
                   system_prompt:str=None, 
                   n_items:int=None,
                   convert2mp3:bool = False,
                   export_mp3_dir:str = None, 
                   show_transcription:bool=False,
                   show_notes:bool=False):
        """
        Transcribes an audio file, summarizes the transcript, and displays the summary.

        Args:
            system_prompt (str, optional): The prompt that is used to generate the summary. Defaults to None.
            n_items (int, optional): The number of summary items to display. Defaults to None.
            convert2mp3 (bool, optional): If True, the audio file is converted to an MP3 file before transcription. Defaults to False.
            export_mp3_dir (str, optional): The directory where the MP3 file is exported, if it is converted. Defaults to None.
            show_transcription (bool, optional): If True, the transcription text is printed to the console. Defaults to False.
            show_notes (bool, optional): If True, the summary is printed to the console. Defaults to False.

        Methods:
            - to_mp3(export_dir:str=None): Converts the audio file to an MP3 file and saves it to the specified export directory.
            - get_filesize(): Returns the size of the audio file in bytes.
            - get_duration(): Returns the duration of the audio file in seconds.
            - transcribe_audio(show_output:bool=False): Transcribes the audio file and saves the transcription text to a class attribute.
            - summarize_text(system_prompt:str=None, n_items:int=None, show_notes:bool=False): Generates a summary of the transcription text using the OpenAI API and saves the summary to a class attribute.
            - save_txt(export_dir:str=None): Saves the transcription or summary text to a .txt file in the specified export directory.

        Examples:
            # Initialize the OpenAI_NoteTaker class with the input directory and summarizer model
            note_taker = OpenAI_NoteTaker(input_dir='path/to/input', summarizer_model='gpt-3')
            
            # Define role_txt for system_prompt
            role_txt = "'You are a graduating SHS student, excellent at summarizing notes in layman's terms."

            # Transcribe the audio file, summarize the transcription, and display the summary
            note_taker.take_notes(system_prompt=role_txt, n_items=3, show_transcription=True, show_notes=True)

        Attributes:
            - input_dir (str): The directory where the input audio file is located.
            - transcriber_model (str): The name of the OpenAI API model used for transcription.
            - USD_per_min (float): The cost in USD per minute of audio transcribed using the OpenAI API.
            - summarizer_model (str): The name of the OpenAI API model used for summarization.
            - USD_per_1k (float): The cost in USD per 1000 tokens generated by the OpenAI API.
            - encoding_name (str): The name of the encoding used by the OpenAI API for summarization.
            - Transcriber (OpenAI_Transcriber): An instance of the OpenAI_Transcriber class.
            - Transcribed_Audio (str): The text of the audio transcription.
            - Summarizer (OpenAI_Summarizer): An instance of the OpenAI_Summarizer class.
        """
        self.Transcriber = OpenAI_Transcriber(input_dir = self.input_dir, 
                                              transcriber_model = self.transcriber_model, 
                                              USD_per_min = self.USD_per_min)
        if convert2mp3==True:
            self.Transcriber.to_mp3(export_dir=export_mp3_dir)
        
        self.Transcriber.get_filesize()
        self.Transcriber.get_duration()
        
        self.Transcriber.transcribe_audio(show_output=show_transcription)
        
        self.Transcribed_Audio = self.Transcriber.transcript_text
        
        self.Summarizer = OpenAI_Summarizer(transcript_text = self.Transcribed_Audio, 
                                            summarizer_model = self.summarizer_model, 
                                            USD_per_1k = self.USD_per_1k, 
                                            encoding_name = self.encoding_name)

        self.Summarizer.num_tokens_from_input_string()
        print(f"Input transcription tokens: {self.Summarizer.input_num_tokens}\n")
        
        if show_notes==True:
            print(f"NoteTaker's Summary in {n_items} points: \n")
            
        self.Summarizer.summarize_text(system_prompt = system_prompt, 
                                       n_items = n_items, 
                                       show_notes = show_notes)
        
    def save_notes(self, 
                   export_transcription_dir:str=None, 
                   export_summary_dir:str=None):
        """
        Saves the transcribed text and summary to text files at the specified directory.
        
        Parameters:
        -----------
        export_transcription_dir : str, optional
            The directory to export the transcribed text file to.
        
        export_summary_dir : str, optional
            The directory to export the summary text file to.
            
        Examples:
        ---------
        # Define role_txt for system_prompt
        role_txt = "'You are a graduating SHS student, excellent at summarizing notes in layman's terms."
        
        # Saving the transcribed text and summary to default directory
        note_taker = OpenAI_NoteTaker(input_dir="path/to/input")
        note_taker.take_notes(system_prompt=role_txt)
        note_taker.save_notes()
        
        # Saving the transcribed text and summary to specified directory
        note_taker = OpenAI_NoteTaker(input_dir="path/to/input")
        note_taker.take_notes(system_prompt="summarize the above text in 3 points")
        note_taker.save_notes(export_transcription_dir="path/to/export/transcription", 
                              export_summary_dir="path/to/export/summary")
        
        Attributes:
        -----------
        None
        """
        self.Transcriber.save_txt(export_dir=export_transcription_dir)
        self.Summarizer.save_txt(export_dir=export_summary_dir)
        
        
    def get_total_job_price(self):
        """
        Calculates the total price of the transcription and summarization job, and prints the breakdown.

        Parameters:
        None.

        Methods:
        - OpenAI_Transcriber.get_price(): Calculate the price of the transcription job.
        - OpenAI_Summarizer.get_price(): Calculate the price of the summarization job.

        Examples:
        1. Calculate and print the total price of the job:
            note_taker = OpenAI_NoteTaker(input_dir="/path/to/input/dir/",
                                          transcriber_model="whisper-1",
                                          USD_per_min=0.006,
                                          summarizer_model="gpt-3.5-turbo",
                                          USD_per_1k=0.002,
                                          encoding_name="cl100k_base")
            note_taker.take_notes(system_prompt="Summarize the text in 5 points.",
                                  n_items=5,
                                  show_transcription=False,
                                  show_notes=True)
            note_taker.get_total_job_price()

        Attributes:
        - self.transcribed_price (float): The price of the transcription job in USD.
        - self.summarization_price (float): The price of the summarization job in USD.
        - self.total_job_price (float): The total price of the job in USD.
        - self.transcribed_price_dict (dict): A dictionary containing the price of the transcription job.
        - self.summarization_price_dict (dict): A dictionary containing the price of the summarization job.
        - self.total_job_price_dict (dict): A dictionary containing the total price of the job.
        - self.complete_job_price_dict (dict): A dictionary containing the breakdown of the job price.
        - self.complete_job_price_dict_USD (dict): A dictionary containing the breakdown of the job price in USD.
        """
        self.Transcriber.get_price()
        self.Summarizer.get_price()
        
        self.transcribed_price = float(self.Transcriber.total_price)
        self.summarization_price = float(self.Summarizer.output_price_dict['total_tokens'])
        self.total_job_price = self.transcribed_price + self.summarization_price
        
        self.transcribed_price_dict = {'transcription_price': self.transcribed_price} 
        self.summarization_price_dict = {'summarization_price': self.summarization_price} 
        self.total_job_price_dict = {'total_job_price': self.total_job_price}
        
        self.complete_job_price_dict = self.transcribed_price_dict | self.summarization_price_dict | self.total_job_price_dict
        self.complete_job_price_dict_USD = {job_type: f"{value:.5f} USD" for job_type, value in self.complete_job_price_dict.items()}
        
        print('\nJob Price Breakdown: \n')
        for job_type,value_USD in self.complete_job_price_dict_USD.items(): 
            print(f"{job_type}: {value_USD}") 