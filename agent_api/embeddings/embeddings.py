from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import json

def leer_vectorstore(path, output):
    print(f"📦 Cargando vector store desde: {path}")
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
    docs = db.similarity_search("mostrar todo", k=len(db.index.reconstruct_n(0, db.index.ntotal)))
    with open(output, "w", encoding="utf-8") as f:
        for i, doc in enumerate(docs):
            f.write(f"=== Documento {i+1} ===\n")
            f.write(f"{doc.page_content}" + "\n")
            f.write(f"Metadata ->{str(doc.metadata)}" + "\n\n")
    print(f"✅ Guardado en {output}")

def ver_embeddings_vectores(path):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    faiss_index = db.index
    vectors = faiss_index.reconstruct_n(0, faiss_index.ntotal)  # todos los vectores
    print(vectors[0])


def guardar_vectorstore():
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    docs = []
    with open("./ai-agent/docs/datos_financieros.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            doc = Document(
                page_content=entry["text"],
                metadata=entry["metadata"]
            )
            docs.append(doc)
    db = FAISS.from_documents(docs, embedding_model)
    db.save_local("./ai-agent/vectorstore_fondos")

try:
    guardar_vectorstore()
    leer_vectorstore("./ai-agent/vectorstore_fondos", "./ai-agent/docs/metadata/embeddings_2_2.txt")
    # ver_embeddings_vectores("vectorstore_fondos")
except Exception as e:
    print(f"Error: {e}")