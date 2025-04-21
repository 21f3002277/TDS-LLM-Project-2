
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import httpx

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow only OPTIONS and POST
    allow_headers=["*"],  # Allow all headers
)

# OpenAI API details
OPENAI_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjMwMDIyNzdAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.K7NIPo5oVym7DFKdql2gXwAgdajEwnzHhEcSFCjc7gw"
OPENAI_API_URL = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"

async def get_embedding(text: str) -> list:
    """Generate text embedding using OpenAI's API via httpx."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": "text-embedding-3-small",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(OPENAI_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to generate embedding.")
        return response.json()["data"][0]["embedding"]

@app.post("/similarity")
async def similarity_endpoint(request: dict):
    try:
        docs = request.get("docs", [])
        query = request.get("query", "")

        if not docs or not query:
            raise HTTPException(status_code=400, detail="Both 'docs' and 'query' must be provided.")

        # Generate embeddings for the query and documents
        query_embedding = np.array(await get_embedding(query)).reshape(1, -1)
        doc_embeddings = [np.array(await get_embedding(doc)).reshape(1, -1) for doc in docs]

        # Compute cosine similarity between the query and each document
        similarities = [cosine_similarity(query_embedding, doc_embedding)[0][0] for doc_embedding in doc_embeddings]

        # Rank documents by similarity scores
        ranked_indices = np.argsort(similarities)[::-1]  # Sort in descending order
        top_3_matches = [docs[i] for i in ranked_indices[:3]]

        return {"matches": top_3_matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  
    