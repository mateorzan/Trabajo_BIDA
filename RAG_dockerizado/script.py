from fastapi import FastAPI, HTTPException
import pymongo
from sentence_transformers import SentenceTransformer
import numpy as np
from scipy.spatial.distance import cosine
import pdfplumber

# Conexión a MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.j3yin.mongodb.net/?retryWrites=true&w=majority")
db = client["Rag"]
collection = db['vectors']

# Cargar el modelo de embeddings
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Inicializar la aplicación FastAPI
app = FastAPI()

# Función para extraer texto de PDFs
def extract_text_from_pdfs(file_paths):
    text_data = []
    for file_path in file_paths:
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_data.append(text)
        except Exception as e:
            print(f"Error al procesar el archivo {file_path}: {e}")
    return text_data

# Guardar los textos y sus embeddings en MongoDB
def save_embeddings_to_mongo(texts, embeddings):
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        document = {
            "text": text,
            "embedding": embedding.tolist()  # Convertir el embedding (numpy array) a lista
        }
        collection.insert_one(document)
        print(f"Documento {i+1} guardado en MongoDB.")

# Consulta por similitud en MongoDB
def query_mongo_by_similarity(query, top_k=3):
    # Generar el vector (embedding) para la consulta
    query_embedding = model.encode([query])[0]
    
    # Recuperar documentos desde MongoDB
    documents = list(collection.find())
    
    # Calcular similitud coseno
    similarities = []
    for doc in documents:
        stored_embedding = np.array(doc['embedding'])
        similarity = 1 - cosine(query_embedding, stored_embedding)
        similarities.append((similarity, doc['text']))
    
    # Ordenar por similitud y devolver los textos más similares como un único string
    similarities.sort(reverse=True, key=lambda x: x[0])
    top_texts = [text for _, text in similarities[:top_k]]
    return "\n".join(top_texts)  # Concatenar los textos con saltos de línea

# Endpoint para procesar archivos PDF y guardarlos en MongoDB
@app.post("/process-pdfs/")
def process_pdfs(file_paths: list[str]):
    texts = extract_text_from_pdfs(file_paths)
    if not texts:
        raise HTTPException(status_code=400, detail="No se pudo extraer texto de los PDFs.")
    
    embeddings = model.encode(texts)
    save_embeddings_to_mongo(texts, embeddings)
    return {"message": f"Se procesaron {len(file_paths)} archivos PDF y se almacenaron en la base de datos."}

# Endpoint para realizar consultas
@app.get("/query/")
def query(query: str, top_k: int = 3):
    try:
        context = query_mongo_by_similarity(query, top_k)
        if not context:
            raise HTTPException(status_code=404, detail="No se encontraron resultados relevantes.")
        return {"query": query, "response": context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")

