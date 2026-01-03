from fastapi import Depends, FastAPI, HTTPException, Header
import uvicorn
from openai_call import Chat_services, HistoryManager, get_History_Storage, get_chat_services
from schemas import ChatRequest, SessionResponse, ChatResponse

app = FastAPI()

@app.post("/session/start", response_model=SessionResponse)
def start_session(
    history_storage: HistoryManager = Depends(get_History_Storage)
):
    """
    Create a new chat session
    """
    session_id = history_storage.create_session()
    return SessionResponse(
        session_id=session_id,
        message="Session created successfully. Use this session_id in X-Session-ID header."
    )

@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    session_id: str = Header(..., alias="X-Session-ID"),
    chat_service: Chat_services = Depends(get_chat_services),
    history_storage: HistoryManager = Depends(get_History_Storage)
):
    """
    Send a query and get AI response with conversation context
    """
    if not history_storage.is_valid_session(session_id):
        raise HTTPException(status_code=401, detail="Invalid or expired session.")
    
    return chat_service.process_user_query(session_id, request.user_query)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)