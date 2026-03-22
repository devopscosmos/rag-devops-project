from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3YM2jgniCG4ij46z6hw7EPV15eIE8ojdvGXi7QEHWRMnBYMXTM8wJQQJ99CCACHrzpqXJ3w3AAABACOGZWFz",
    api_version="2024-02-15-preview",
    azure_endpoint="https://openai-rag-northcentralus.openai.azure.com/"
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Explain what RAG is in 2 sentences"}
    ]
)

print(response.choices[0].message.content)
