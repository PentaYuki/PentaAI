
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str

app = FastAPI()

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/ecosystem/apps")
async def get_apps():
    return {"apps": ["Pentaschool", "Pentanote", "PentaKuRu", "PentaMarket", "PentaJob"]}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    return {"response": f"Received: {request.query}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
