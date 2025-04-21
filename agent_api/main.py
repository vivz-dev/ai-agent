from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import agent_api.agent.assistant as assistant
from fastapi.middleware.cors import CORSMiddleware
import agent_api.data.session_store as ss

app = FastAPI()

class ChatRequest(BaseModel):
    user_input: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.user_input
    try:
        assistant_reply = assistant.chatear(user_input)
        print(assistant_reply)
        # print(ss.get_responses())
        for mensaje in ss.get_responses():
            print(mensaje)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"reply": assistant_reply,
            "historial": ss.historial_responses}