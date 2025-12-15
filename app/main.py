from fastapi import FastAPI

app= FastAPI(title="Todo List API")

@app.get("/")
def root():
    return {"message":"Todo List API is running"}

