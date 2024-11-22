import openai
from werkzeug.datastructures import FileStorage

class Transcriber:
    def __init__(self):
        pass

    def transcribe(self, audio: FileStorage) -> str:
        if not audio:
            raise ValueError("No se recibió un archivo de audio válido.")
        try:
            audio.save("audio.mp3")
            audio_file = open("audio.mp3", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            return transcript.text
        except Exception:
            return "Hubo un error al procesar el audio. Por favor, intenta nuevamente."
