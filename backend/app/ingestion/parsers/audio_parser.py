#from app.ingestion.connectors.audio import transcribe_audio
from groq import Groq
import os
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
load_dotenv()

class AudioParser:
    def __init__(self):
        self.client= Groq(api_key=os.getenv("GROQ_API_KEY"))
        
    def transcribe_audio(self, audio_path:str | Path) ->Dict:
        
        file_name = Path(audio_path)
        
        try:
            with open(file_name,"rb") as audio_file:
                completion= self.client.audio.transcriptions.create(
                    model = "whisper-large-v3-turbo",
                    file= audio_file,
                    response_format = "verbose_json",
                    temperature=0.0
                )
                print(f"DEBUG -- audio file recieved in transcribed_audio: {file_name}")
                
            return {
                "text":completion.text.strip(),
                "source": "audio",
                "filename":audio_file.name,
                "language":getattr(completion, "language", None),
                "duration":getattr(completion, "duration", None),
                "file_path": str(audio_path)
            }
            
        except Exception as e:
            error_msg = f"Error in transcription: {e}"
            print(error_msg)
            return error_msg

        


audio_parser = AudioParser()