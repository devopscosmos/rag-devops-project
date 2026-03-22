import json
import numpy as np
import faiss
from openai import AzureOpenAI

endpoint="https://openai-rag-northcentralus.openai.azure.com/"
api_key="3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz"

chat_model="gpt-4.1-mini"
embedding_model="text-embedding-3-small"

client=AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=endpoint
)

index=faiss.read_index("vector_index.faiss")

with open("chunks.json") as f:
    chunks=json.load(f)

query=input("Ask a question: ")

query_emb=client.embeddings.create(
    model=embedding_model,
    input=query
)

query_vector=np.array([query_emb.data[0].embedding]).astype("float32")

D,I=index.search(query_vector,k=3)

context=" ".join([chunks[i] for i in I[0]])

response=client.chat.completions.create(
    model=chat_model,
    messages=[
        {"role":"system","content":"Answer from the provided context"},
        {"role":"user","content":f"Context:{context}\n\nQuestion:{query}"}
    ]
)

print("\nAnswer:\n")
print(response.choices[0].message.content)