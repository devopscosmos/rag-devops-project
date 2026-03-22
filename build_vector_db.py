import os
import json
import numpy as np
import faiss
from pypdf import PdfReader
from openai import AzureOpenAI
import pickle

endpoint="https://openai-rag-northcentralus.openai.azure.com/"
api_key="3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz"

chat_model="gpt-4.1-mini"
embedding_model="text-embedding-3-small"

client=AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=endpoint
)

folder="docs"

docs=[]

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        reader=PdfReader(os.path.join(folder,file))
        for page in reader.pages:
            text=page.extract_text()
            docs.append(text)

# simple chunking
def split_text(doc, chunk_size=400, overlap=100):
    words = doc.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


chunks = []

for doc in docs:
    if doc:  # skip empty text
        chunks.extend(split_text(doc))

print("Total chunks:",len(chunks))

embeddings=[]

for i, chunk in enumerate(chunks[:]):

    print(f"Embedding {i+1}/{len(chunks)}")

    emb=client.embeddings.create(
        model=embedding_model,
        input=chunk
    )

    embeddings.append(emb.data[0].embedding)

embeddings=np.array(embeddings).astype("float32")

index=faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

faiss.write_index(index,"vector_index.faiss")

with open("chunks.json","w") as f:
    json.dump(chunks,f)

with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)
print("Vector database built successfully")