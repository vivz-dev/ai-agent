from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import agent.assistant as assistant

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
    
query1 = "cual fue el porcentaje de variación de cartera de credito de banco guayaquil en el Q1 y Q2 de hace 5 años atrás?"
query2 = "dame un resumen de lo que pasó en los balances del Q1 y Q2 de hace 5 años atrás?"
query3 = "compara el año pasado con este"
query4 = "hola"

# assistant.chatear("dame un resumen de lo que pasó en los balances del Q1 y Q2 de hace 5 años atrás?")
# assistant.chatear("dime como fueron los activos de junio y octubre 2023")