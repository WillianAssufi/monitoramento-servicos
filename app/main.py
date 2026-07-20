from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def obter_status():
    return {"status": "online"}