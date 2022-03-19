from typing import Optional

from fastapi import FastAPI
import requests
import io

import LogoExtractor

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/logo/{item_id}")
def read_q(q: Optional[str] = None):
    im_url = LogoExtractor.get_icpyton(q)
    return {"url": im_url}


@app.get("/create/{item_id}")
def read_q(q: Optional[str] = None):
    return {"url": q}
