import os
import openai
from pydub import AudioSegment
import wave
import magic

class OpenAI_Transcriber:
    """
    This class provides methods for transcribing an audio file using OpenAI's
    transcription service. The class supports automatic conversion of input files
    to MP3 format, retrieval of file size and duration, estimation of the cost
    of transcription, transcription of the audio file, and saving the transcript
    to a text file.
    
    -----------
    Parameters:
    -----------
    
    - input_dir (str): The file path to the audio file to be transcribed.
    - transcriber_model (str): The name of the transcriber model to use. Defaults to "whisper-1".
    - USD_per_min (float): The cost per minute in USD for using the transcriber service. Defaults to 0.006.
    
    --------
    Methods:
    --------
    
    - to_mp3(export_dir=None): Converts the input audio file to MP3 format if necessary.
    - get_filesize(): Returns the file size of the input audio file in megabytes.
    - get_duration(): Returns the duration of the input audio file in seconds.
    - get_price(): Calculates the total price of the transcription service based on the duration of the input audio file.
    - transcribe_audio(show_output=False): Transcribes the input audio file using the specified transcriber model.
    - save_txt(export_dir=None): Saves the transcription output to a text file.
    
    -----------
    Attributes:
    -----------
    
    - input_dir (str): The file path to the input audio file.
    - transcriber_model (str): The name of the transcriber model used.
    - USD_per_min (float): The cost per minute in USD for using the transcriber service.
    - filepath_mp3 (str): The file path to the MP3 version of the input audio file.
    - input_filesize (float): The file size of the input audio file in megabytes.
    - duration (float): The duration of the input audio file in seconds.
    - transcript (dict): The output of the transcription service, including the transcription text and confidence score.
    - transcript_text (str): The transcription text output only.
    - filepath_txt (str): The file path to the saved text file containing the transcription output.
    
    ---------
    Examples:
    ---------
    
    # Create an instance of the OpenAI_Transcriber class
    transcriber = OpenAI_Transcriber(input_dir="audio_file.wav")
    
    # Convert the input file to MP3 format
    transcriber.to_mp3()
    
    # Get the duration of the input file
    transcriber.get_duration()
    
    # Get the price of the transcription service
    transcriber.get_price()
    
    # Transcribe the input file
    transcriber.transcribe_audio()
    
    # Save the transcription output to a text file
    transcriber.save_txt()

    """
    def __init__(self, 
                 input_dir:str, 
                 transcriber_model:str = "whisper-1", 
                 USD_per_min:float = 0.006):
        """
        Initializes the OpenAI_Transcriber class.

        Parameters:
        ----------
        input_dir: str
            The directory path of the input audio file.
        transcriber_model: str, optional (default="whisper-1")
            The OpenAI transcriber model to use. Default is "whisper-1".
        USD_per_min: float, optional (default=0.006)
            The price per minute for transcribing audio. Default is 0.006 USD per minute.

        Returns:
        -------
        None
        """
        self.input_dir = input_dir
        self.transcriber_model = transcriber_model
        self.USD_per_min = USD_per_min
        
        self.audio_file = open(self.input_dir, "rb")
        self.filetype = magic.Magic(mime=True).from_file(self.input_dir)
        
    def to_mp3(self, export_dir=None):
        """
        Convert the input audio file to MP3 format using ffmpeg.

        Args:
            export_dir (str, optional): If specified, the path to save the MP3 file.
                                        If None, the MP3 file is saved in the same directory
                                        as the input file with the same name but with .mp3 extension.
                                        Defaults to None.

        Returns:
            None

        Raises:
            Exception: Raised if an error occurs during the conversion process.

        """
        if self.filetype == "audio/mpeg":
            print("File is already in mp3 format.")
            
        else:
            try:
                self.audiosegment = AudioSegment.from_file(self.input_dir, self.filetype.split('/')[1])
        
                if export_dir==None:
                    self.filepath_mp3 = self.input_dir.replace(self.input_dir.split('.')[-1],'mp3')
                    self.audiosegment.export(self.filepath_mp3, format="mp3")

                else:
                    self.filepath_mp3 = export_dir
                    self.audiosegment.export(self.filepath_mp3, format="mp3")

                self.audio_file = open(self.filepath_mp3, "rb")
                self.filetype = magic.Magic(mime=True).from_file(self.filepath_mp3)
                
                print(f"Output .mp3 file saved to {self.filepath_mp3}")
                print("Conversion to mp3 successful.")
                
                self.input_dir = self.filepath_mp3
                
            except Exception as e:
                print("Error converting file to mp3.")
                print(e)
        
                
    def get_filesize(self):
        """
        Get the file size of the input audio file.
        
        Returns
        -------
        None
        
        Prints
        ------
        input_filesize : float
            The size of the input audio file in MB.
        """
        self.input_filesize = os.stat(self.input_dir).st_size / (1024 * 1024)
        print(f"Input file size: {self.input_filesize:.2} MB.")
        
            
    def get_duration(self):
        """
        Gets the duration of the input audio file.
        
        Raises:
            OSError: If the file cannot be opened or read.
            TypeError: If the file type is not supported.
        
        Prints:
            The duration of the audio file in seconds.
        """
        try:
            if self.filetype == "audio/wav" or self.filetype == "audio/x-wav":
                with wave.open(self.input_dir, 'r') as f:
                    frames = f.getnframes()
                    rate = f.getframerate()
                    self.duration = frames / float(rate)
                    print(f'Duration: {self.duration:.2} s')
            else:
                audio = AudioSegment.from_file(self.input_dir)
                self.duration = audio.duration_seconds
                print(f'Duration: {self.duration:.2} s')
                
        except:
            print("Error getting file length.")
    
    def get_price(self):
        """
        Calculates the total cost of transcribing the audio based on its duration and the given USD per minute rate.

        Raises:
            None

        Returns:
            None
        """
        self.total_price = self.duration * (self.USD_per_min/60.0)
        
    def transcribe_audio(self, 
                         show_output=False):
        """
        Transcribes the audio file using the specified transcriber model.

        Args:
            show_output (bool, optional): If True, prints the transcribed text. Defaults to False.

        Returns:
            None
        """
        self.transcript = openai.Audio.transcribe(self.transcriber_model, 
                                                  self.audio_file)
        
        self.transcript_text = self.transcript['text']
        
        if show_output==True:
            print(self.transcript_text)
            
    def save_txt(self, export_dir=None): 
        """
        Saves the transcript text to a text file.
        
        Parameters:
        -----------
        export_dir: str, optional
            The export directory of the output .txt file. If None, 
            the directory will be the same as the input audio file.
        
        Returns:
        --------
        None
        """
        if export_dir is None:
            self.filepath_txt = self.input_dir.replace(self.input_dir.split('.')[-1],' txt')
        else:
            self.filepath_txt = f"{export_dir}.txt"
        
        with open(self.filepath_txt, 'w', encoding="utf-8") as f:
            f.write(self.transcript_text)
            f.close()
        
        print(f"Transcript saved at: {self.filepath_txt}")