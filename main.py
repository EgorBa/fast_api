import io
from typing import Optional
from PIL import Image
from fastapi import FastAPI
from random import randrange
import LogoExtractor
from VideoCreator import generate_one_video
from pydantic import BaseModel
import firebase_admin
from firebase_admin import db
import threading

cred_object = firebase_admin.credentials.Certificate('panelcreama-firebase-adminsdk-pxxap-8daf8c0b6c.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': 'https://panelcreama-default-rtdb.firebaseio.com'
})

diversity = 1000000
app = FastAPI()


def func_launch_video(image, descr):
    video_len = 4
    W = 720
    H = 1280

    input_path = get_path("in")
    inp = io.BytesIO(image.encode('ISO-8859-1'))
    imageFile = Image.open(inp)
    imageFile.save(input_path)
    imageFile.close()

    path_1 = generate_one_video(
        video_len,
        x1=0, y1=0, x2=W, y2=int(H / 3),  # text position
        x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
        text=descr,  # text
        path_to_image=input_path,  # path to image
        animation_type='simple',  # type of animation
        url='https://pythonist.ru'
    )

    imageFileObj = open(path_1, 'rb')
    imageBinaryBytes = imageFileObj.read()
    imageStream = io.BytesIO(imageBinaryBytes)
    s = imageStream.read().decode('ISO-8859-1')

    db.reference("/").child("videos").child(str(id)).set(s)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


def get_path(tag):
    return str(randrange(diversity)) + "_" + tag + ".png"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/logo/{item_id}")
def read_q(q: Optional[str] = None):
    im_url = LogoExtractor.get_icon(q)
    return {"url": im_url}


@app.post("/item/")
async def create_item(item: Item):
    return item


@app.get("/generate/{item_id}")
def read_request(id: Optional[int] = 0):
    if id == 0:
        return {"": ""}

    image = db.reference("/").child("images").child(str(id)).get("image")[0]['image']
    descr = db.reference("/").child("images").child(str(id)).get("descr")[0]['descr']

    video_len = 4
    W = 720
    H = 1280

    input_path = get_path("in")
    out_file = open(input_path, "wb")
    out_file.write(image.encode('ISO-8859-1'))
    out_file.close()

    path_1 = generate_one_video(
        video_len,
        x1=0, y1=0, x2=W, y2=int(H / 3),  # text position
        x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
        text=descr,  # text
        path_to_image=input_path,  # path to image
        animation_type='simple',  # type of animation
        url='https://pythonist.ru'
    )

    imageFileObj = open(path_1, 'rb')
    imageBinaryBytes = imageFileObj.read()
    imageStream = io.BytesIO(imageBinaryBytes)
    s = imageStream.read().decode('ISO-8859-1')

    db.reference("/").child("videos").child(str(id)).set(s)

    return {"video": "generating"}


@app.get("/create/{item_id}")
def read_request(im1: Optional[str] = "", im2: Optional[str] = "", im3: Optional[str] = "",
                 desc1: Optional[str] = "", desc2: Optional[str] = "", desc3: Optional[str] = "",
                 url: Optional[str] = ""):
    video_len = 4
    W = 720
    H = 1280

    if im1 != "":
        input_path = get_path("in")
        inp = io.BytesIO(im1.encode('ISO-8859-1'))
        imageFile = Image.open(inp)
        imageFile.save(input_path)
        imageFile.close()

        path_1 = generate_one_video(
            video_len,
            x1=0, y1=0, x2=W, y2=int(H / 3),  # text position
            x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
            text=desc1,  # text
            path_to_image=input_path,  # path to image
            animation_type='simple',  # type of animation
            url='https://pythonist.ru'
        )

        imageFileObj = open(path_1, 'rb')
        imageBinaryBytes = imageFileObj.read()
        imageStream = io.BytesIO(imageBinaryBytes)
        s = imageStream.read().decode('ISO-8859-1')
        return {"video": s}

    else:
        path_1 = generate_one_video(
            video_len,
            x1=0, y1=0, x2=W, y2=int(H / 3),  # text position
            x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
            text=desc1,  # text
            path_to_image="logos/0.png",  # path to image
            animation_type='simple',  # type of animation
            url='https://pythonist.ru'
        )
        imageFileObj = open(path_1, 'rb')
        imageBinaryBytes = imageFileObj.read()
        imageStream = io.BytesIO(imageBinaryBytes)
        s = imageStream.read().decode('ISO-8859-1')
        return {"video": s}
