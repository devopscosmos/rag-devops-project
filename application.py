from fastapi import FastAPI
from pydantic import BaseModel
import faiss
from openai import AzureOpenAI
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import pickle

app = FastAPI()

# Request format
class QueryRequest(BaseModel):
    question: str

# Load FAISS index
index = faiss.read_index("vector_index.faiss")

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Azure OpenAI client (reuse your config)
client = AzureOpenAI(
    api_key="3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz",
    api_version="2024-02-01",
    azure_endpoint="https://openai-rag-northcentralus.openai.azure.com/"
)

@app.post("/ask")
def ask_question(request: QueryRequest):
    question = request.question

    # 1. Create embedding
    emb = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    )

    query_vector = emb.data[0].embedding

    # 2. Search FAISS
    query_vector = np.array(query_vector).astype("float32").reshape(1, -1)  
	## above line added for application.py# wasnt there for app.
    #D, I = index.search([query_vector], k=3) #was for app.py
    D, I = index.search(query_vector, k=2)  #changeing k=2 from k=3 to get answers fast
    print("Retrieved chunks:", I[0])
    # 3. (Simplified) context
    #context = "Relevant chunks from your docs here" #old1
    context = "\n\n".join([chunks[i][:500] for i in I[0]]) ## to get fanswers fast

    # 4. Ask GPT
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
    {
        "role": "system",
        "content": "Answer using the provided context. If partially relevant, try to answer. If completely unrelated, say 'Not found in document'."
    },
    {
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion:\n{question}"
    }
]
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content
    }
	
##To get answer format corectly/ not empty string after clicking on 'Ask' button on UI (double click on index.html(open file))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"status": "RAG API running"}
