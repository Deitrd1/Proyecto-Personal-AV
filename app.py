import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

# Cargar llaves del archivo .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    # Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    if not audio:
        return {"result": "error", "text": "No se recibió ningún archivo de audio."}

    text = Transcriber().transcribe(audio)
    
    # Utilizar el LLM para ver si llamar una función
    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name == "get_weather":
        # Llamar a la función del clima
        function_response = Weather().get(args.get("ubicacion"))
        final_response = llm.process_response(text, message, function_name, json.dumps(function_response))
    elif function_name == "open_chrome":
        # Llamar a la función para abrir Chrome
        PcCommand().open_chrome(args.get("website"))
        final_response = f"Listo, ya abrí Chrome en el sitio {args.get('website')}"
    else:
        # Respuesta genérica para entradas no válidas
        final_response = "Lo siento, no entendí tu solicitud. Por favor, intenta ser más específico."

    # Generar respuesta de texto a voz
    tts_file = TTS().process(final_response)
    return {"result": "ok", "text": final_response, "file": tts_file}

if __name__ == "__main__":
    app.run(debug=True)
