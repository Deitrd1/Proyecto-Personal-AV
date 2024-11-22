import openai
import json

class LLM:
    def __init__(self):
        pass

    def process_functions(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en videojuegos con más de 20 años de experiencia, eres amable, educado, y puedes entablar conversaciones relacionadas con videojuegos con naturalidad."},
                {"role": "user", "content": text},
            ],
            functions=[
                {
                    "name": "get_weather",
                    "description": "Obtener el clima actual",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ubicacion": {"type": "string", "description": "La ubicación, debe ser una ciudad"}
                        },
                        "required": ["ubicacion"],
                    },
                },
                {
                    "name": "open_chrome",
                    "description": "Abrir el explorador Chrome en un sitio específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "website": {"type": "string", "description": "El sitio al cual se desea ir"}
                        },
                        "required": ["website"],
                    },
                }
            ],
            function_call="none",
        )

        message = response["choices"][0]["message"]
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = json.loads(message["function_call"]["arguments"])
            return function_name, args, message

        return None, None, message

    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un experto en videojuegos con más de 20 años de experiencia, eres amable, educado, y puedes entablar conversaciones relacionadas con videojuegos con naturalidad."},
                {"role": "user", "content": text},
                message,
                {"role": "function", "name": function_name, "content": function_response},
            ],
        )
        return response["choices"][0]["message"]["content"]


#TT