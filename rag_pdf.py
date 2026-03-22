import os
import numpy as np
import faiss
from pypdf import PdfReader
from openai import AzureOpenAI

# Azure OpenAI config
endpoint = "https://openai-rag-northcentralus.openai.azure.com/"
api_key = "3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz"
chat_deployment = "gpt-4.1-mini"
embedding_deployment = "text-embedding-3-small"

client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=endpoint
)

# Read PDF files
docs = []
folder = "docs"

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        reader = PdfReader(os.path.join(folder, file))
        for page in reader.pages:
            docs.append(page.extract_text())

# Create embeddings
embeddings = []
for doc in docs:
    emb = client.embeddings.create(
        model=embedding_deployment,
        input=doc
    )
    embeddings.append(emb.data[0].embedding)

embeddings = np.array(embeddings).astype("float32")

# Create vector index
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# Ask question
query = input("Ask a question: ")

query_emb = client.embeddings.create(
    model=embedding_deployment,
    input=query
)

query_vector = np.array([query_emb.data[0].embedding]).astype("float32")

# Search similar doc
D, I = index.search(query_vector, k=1)
context = docs[I[0][0]]

# Ask GPT
response = client.chat.completions.create(
    model=chat_deployment,
    messages=[
        {"role": "system", "content": "Answer using the provided document context."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
    ]
)

print("\nAnswer:\n")
print(response.choices[0].message.content)