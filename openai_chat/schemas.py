from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_query: str
    
class SessionResponse(BaseModel):
    message: str
    session_id: str
        
class ChatResponse(BaseModel):
    session_id: str
    user_query: str
    response: str
