import uuid
from fastapi import Depends, HTTPException
from openai import OpenAI
from typing import Dict, List, Annotated
from functools import lru_cache 
from config import API_KEY, MODEL_NAME
from schemas import ChatResponse 

class HistoryManager:
    def __init__(self):
        self.history: Dict[str, List[Dict[str, str]]] = {}
        self.active_sessions: set = set()

    def create_session(self):
        session_id = uuid.uuid4().hex
        self.active_sessions.add(session_id)
        self.history[session_id] = []
        return session_id
    
    def is_valid_session(self, session_id: str) -> bool:
        return session_id in self.active_sessions
    
    def add_message_to_history(self, session_id: str, role : str, content : str):
        if session_id not in self.history:
            self.history[session_id] = []
        self.history[session_id].append({"role": role, "content": content})
            
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.history.get(session_id, [])        

class OpenAI_Service:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)
                        
    def get_openai_response(self, message: List[Dict[str,str]]) -> str:
        try:    
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=message,
                temperature=0.3,
                max_tokens=500,
            )
            return response.choices[0].message.content 
        except Exception as e:
            print(f"OpenAI Error: {e}")
            raise HTTPException(status_code=500, detail="OpenAI API error")
        
class Chat_services:
    def __init__(self, openai_service: OpenAI_Service, history_service: HistoryManager):
        self.openai_services = openai_service
        self.history_service = history_service

    def process_user_query(self, session_id: str, user_query: str) -> ChatResponse:
        if not self.history_service.is_valid_session(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        history = self.history_service.get_history(session_id)
        
        messages_payload = history + [{"role": "user", "content": user_query}]
        
        ai_response = self.openai_services.get_openai_response(messages_payload)
        
        self.history_service.add_message_to_history(session_id, "user", user_query)
        self.history_service.add_message_to_history(session_id, "assistant", ai_response)
        
        return ChatResponse(
            session_id=session_id,
            user_query=user_query,
            response=ai_response
        )


def get_openai_service() -> OpenAI_Service:
    return OpenAI_Service()

@lru_cache()
def get_History_Storage() -> HistoryManager:   
    return HistoryManager()

def get_chat_services(
    openai_services: OpenAI_Service = Depends(get_openai_service), 
    history_services: HistoryManager = Depends(get_History_Storage)
    ) -> Chat_services:
    return Chat_services(openai_services, history_services)