import pymongo
from flask import Flask, request, jsonify
import ollama


app = Flask(__name__)

# Configuración de MongoDB Atlas
MONGO_URI = "mongodb+srv://admin:admin@cluster0.j3yin.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client["Rag"]
collection = db['dockerizado']

# Función para obtener información relevante desde MongoDB
def retrieve_from_mongo(query):
    results = collection.find({"$text": {"$search": query}})
    return " ".join([result['text_field'] for result in results])

# Función para generar la respuesta usando Ollama
def generate_response(query):
    # Obtener documentos relevantes de MongoDB
    relevant_info = retrieve_from_mongo(query)

    # Concatenar la consulta y la información relevante
    input_text = f"Query: {query}\nRelevant Information: {relevant_info}"

    # Llamar a Ollama para generar la respuesta
    response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": input_text}])
    return response['text']

@app.route('/rag', methods=['POST'])
def rag_endpoint():
    # Obtener la consulta desde la solicitud
    query = request.json.get('query', '')
    
    # Generar la respuesta usando Ollama
    response = generate_response(query)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)

