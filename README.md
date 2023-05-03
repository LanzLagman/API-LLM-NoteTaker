# API-LLM-NoteTaker

A set of Python classes for transcribing and summarizing audio and video files using OpenAI APIs via [Whisper-1](https://openai.com/research/whisper) and [GPT-3.5 turbo](https://platform.openai.com/docs/models/gpt-3-5), in which the latter is a large language model (LLM). I made these tools for our org, the [UP Data Science Society (PU DSSoc)](https://ph.linkedin.com/company/updatasciencesociety), and I'm currently using these in our activities, specifically in taking notes from our meetings and mentorship sessions. This is also my first project wherein I've extensively used ChatGPT for assistance in creating markdowns and docstrings, and I intend to do so for my next open-source projects.

This repo contains a series of Jupyter Notebook tutorials on how I made these classes, building up on summarizing the answers that the panelists gave to my question at [Destination Lakehouse Pilipinas](https://www.linkedin.com/posts/plewniak_lakehouse-bigdataengineer-datascientists-activity-7033623397955768321-gHq_) panel interview. Next, I provided use cases on how this NoteTaker could be used to summarize recorded lectures such as our [Data Ethics](https://www.facebook.com/100079165176241/videos/643438693861938) Mentorship Session at UP DSSoc, and the [Third Biyahenihan Research Forum](https://www.facebook.com/MoveAsOneCoalition/photos/a.133634771718805/778763060539303) ([livestreamed here](https://www.facebook.com/MoveAsOneCoalition/videos/1050324429141251)), in which we presented our reseach paper entitled [Empowering Citizens to Build Better Bike Lanes Through Open Vontracting](https://wesolve.ph/empowering-citizens-to-build-better-bike-lanes-through-open-contracting).  

## Installation
* Install dependencies first before installing the NoteTaker.

### Dependencies
* [openai](https://pypi.org/project/openai/): provides access to the OpenAI Whisper-1 and GPT-3.5 APIs.
* [tiktoken](https://pypi.org/project/tiktoken/): BPE tokeniser for use with OpenAI's models.
* [pydub](https://pypi.org/project/pydub/): for working with audio files.
* [python-magic-bin](https://pypi.org/project/python-magic/): Python interface to the libmagic file type identification library.
* [Wave](https://pypi.org/project/Wave/): module for working with WAV files.
* [python-ffmpeg](https://pypi.org/project/python-ffmpeg/): wrapper around the FFmpeg command line multimedia framework.


### Install via git
```
git clone https://github.com/LanzLagman/API-LLM-NoteTaker.git
cd API-LLM-NoteTaker
```

## How to Use

* On your Jupyter Notebook, load your OpenAI API key saved on a .txt file.
```
with open('api-key.txt', 'r') as file:
    api_key = file.read()

os.environ["OPENAI_API_KEY"] = api_key
openai.api_key = os.getenv("OPENAI_API_KEY")
```

* Import NoteTaker
```
from OpenAI_NoteTaker import OpenAI_NoteTaker
```

* Prepare `role_txt`, the prompt in which you set the behavior of the NoteTaker.
```
role_txt = "You are a detail-oriented STEM student from the Philippines who wants to pursue a career as a data scientist who also specializes in science communication, which allows you to easily transcribe text to pure English."
```

* Initialize an instance of `OpenAI_NoteTaker` as `QnA_NoteTaker`, in which the input file is the `.mp4` file of the Q&A portion of the recorded talk about Data Ethics.
```
QnA_NoteTaker = OpenAI_NoteTaker(input_dir='Data/Input/DSSoc Mentorship/Mentorship_Vid_Pt2.mp4')
```

* Summarize into 6 points using the `take_notes()` method, with `convert2mp3=True` to convert first to `.mp3` file, then define the destination of the `.mp3` file which will then be used for note-taking.
```
QnA_NoteTaker.take_notes(system_prompt=role_txt, 
                         n_items=6, 
                         convert2mp3=True,
                         export_mp3_dir='Data/Output/DSSoc Mentorship/Mentorship_Vid_Pt2.mp3',
                         show_notes=True)
```

* Output
```
Output .mp3 file saved to Data/Output/DSSoc Mentorship/Mentorship_Vid_Pt2.mp3
Conversion to mp3 successful.
Input file size: 2.3e+01 MB.
Duration: 1.5e+03 s
Input transcription tokens: 3894

NoteTaker's Summary in 6 points: 

1. The speaker highlights the importance of ethical considerations in data science.
2. The speaker emphasizes the need for consent and privacy when collecting and analyzing data.
3. The ethical issues surrounding web scraping are discussed, and the importance of analyzing the purpose and content of web-scraped information is emphasized.
4. The speaker recommends the text "Raw Data is an Oxymoron" and the work of Luciano Floridi for those interested in learning more about data ethics.
5. The importance of developing domain-specific knowledge and interdisciplinary skills is stressed.
6. The speaker recommends learning the programming language R.
CPU times: total: 6.48 s
```

* Save raw transcription and summarized notes.
```
QnA_NoteTaker.save_notes(export_transcription_dir='Data/Output/DSSoc Mentorship/Mentorship_Vid_Pt2 [Transcribed]', 
                         export_summary_dir='Data/Output/DSSoc Mentorship/Mentorship_Vid_Pt2 [Notes]')
```

* View total pricing.
```
QnA_NoteTaker.get_total_job_price()
```

* Output price
```
Transcript saved at: Data/Output/DSSoc Mentorship/Mentorship_Vid_Pt2 [Transcribed].txt
Summarized note saved at: Data/Output/DSSoc Mentorship/Mentorship_Vid_Pt2 [Notes].txt

Job Price Breakdown: 

transcription_price: 0.15260 USD
summarization_price: 0.00816 USD
total_job_price: 0.16076 USD
```
