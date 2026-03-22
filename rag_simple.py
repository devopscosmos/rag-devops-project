import numpy as np
import faiss
from openai import AzureOpenAI

# Azure OpenAI config
endpoint = "https://openai-rag-northcentralus.openai.azure.com/"
api_key = "3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz"
deployment = "gpt-4.1-mini"

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=endpoint
)

# Example documents
docs = [
    "Kubernetes Horizontal Pod Autoscaler scales pods based on CPU utilization.",
    "Azure DevOps provides CI/CD pipelines for building and deploying applications.",
    "Docker is used to containerize applications."
]

# Create embeddings
embeddings = []
for doc in docs:
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )
    embeddings.append(emb.data[0].embedding)

# Convert to numpy
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# User question
query = "What does Kubernetes HPA do?"

query_emb = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_vector = np.array([query_emb.data[0].embedding]).astype("float32")

# Search similar document
D, I = index.search(query_vector, k=1)
context = docs[I[0][0]]

# Send to GPT model
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "Answer using the provided context."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
    ]
)

print(response.choices[0].message.content)