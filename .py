function_name, args, message = llm.process_functions(text)
if function_name == "funcion_prueba":
# Llamar a la función que se está probando
function_response = Ver código
final_response = llm.process_response(text, message, function_name, json.dumps(function_response))