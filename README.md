# 📝 Trabajo_BIDA | Proyecto RAG (Retrieve and Generate)

Este proyecto está diseñado para trabajar con la extracción y generación de información utilizando bases de datos Chroma y archivos PDF y datos Web. La estructura de archivos y carpetas se organiza de la siguiente manera:

---

## 📂 Estructura de directorios y archivos

### 📂 Directorios principales

1. **📂 Nba**

   - Contiene bases de datos relacionadas con información de la NBA.
   - **Archivos**:
     - 🗄️ `chroma.sqlite3`: Base de datos Chroma específica de este conjunto.
2. **📂 Pdfs**

   - Contiene bases de datos y documentos PDF relacionados con diferentes temas.
   - **Archivos**:
     - 🗄️ `chroma.sqlite3`: Base de datos Chroma específica de los documentos PDF.

---

### 📄 Archivos principales

1. **📒 Jupyter Notebooks**

   - `RAG_con_GUI.ipynb`: Implementación de la extracción y generación de información con una interfaz gráfica.
   - `RAG_pdf_Castellano.ipynb`: Script para el procesamiento de documentos PDF en español.
   - `RAG_web_Ingles.ipynb`: Script para la extracción de información desde la web en inglés.
2. **📂 Documentos PDF**

   - `archivo_descargado_NBATAST.pdf`: Documento descargado relacionado con la NBA.
   - `archivo_descargado_jugones.pdf`: Documento descargado relacionado con contenido deportivo.
3. **📜 Archivo de licencia**

   - `LICENSE`: Contiene la información sobre la licencia del proyecto.

---

## 🚀  Uso del proyecto

### 🛠️ Requisitos previos

1. Tener instalados Python y las dependencias necesarias. Se recomienda usar entornos virtuales como Conda.
2. Bases de datos Chroma configuradas y funcionando correctamente.

### Configuración

1. Clona este repositorio en tu máquina local.
2. Disponer de una instacia de Docker con una LLM ollama, en este caso se utiliza llama3.2.

### Ejecución

- Ejecutar las celdas de los diferentes notebooks.
