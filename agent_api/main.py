from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import agent_api.agent.assistant as assistant

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.user_input
    try:
        assistant_reply = assistant.chatear(user_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"reply": assistant_reply}