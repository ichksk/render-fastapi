import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)))) #srcを絶対importできるようにする

from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from sqlmodel import create_engine, SQLModel
from ws import updater

engine = create_engine(os.environ["DATABASE_URL"], echo=True)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.websocket("/ws/join")
async def websocket_endpoint(websocket: WebSocket):
    print("join")
    await updater.subscribe("join", websocket)