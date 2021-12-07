from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'Hello' : 'world!'}

@app.get('/ping')
def ping():
    return {'message' : 'pong'}