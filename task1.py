from fastapi import FastAPI, Path
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/user/{user_id}")   # path parameter
def get_user_id(user_id:int = Path(..., description="The ID of the user to retrieve", gt=0)):
    return {"user_id": user_id}

@app.get("/items")
def get_items(skip: int, limit: int):
    return {"skip": skip, "limit": limit}

if __name__ == "__main__":
    uvicorn.run("task1:app", host="127.0.0.1", port=8000, reload=True)