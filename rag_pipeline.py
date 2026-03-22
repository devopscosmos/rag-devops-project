from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.documents import Document

# Sample text (later we will replace with PDF)
text = """
Kubernetes Horizontal Pod Autoscaler automatically scales the number
of pods based on CPU utilization or other metrics.
"""

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = [Document(page_content=text)]
documents = text_splitter.split_documents(docs)

# Create embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://openai-rag-northcentralus.openai.azure.com/",
    api_key="3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz",
    api_version="2024-02-15-preview"
)

# Create vector store
vectorstore = FAISS.from_documents(documents, embeddings)

# User query
query = "What is Kubernetes HPA?"

# Retrieve relevant docs
results = vectorstore.similarity_search(query)

# Send to model
llm = AzureChatOpenAI(
    azure_endpoint="https://openai-rag-northcentralus.openai.azure.com/",
    api_key="3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz",
    api_version="2024-02-15-preview",
    deployment_name="gpt-4.1-mini"
)

response = llm.invoke(query + "\nContext: " + results[0].page_content)

print(response.content)