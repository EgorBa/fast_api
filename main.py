import io
from typing import Optional
from PIL import Image
from fastapi import FastAPI
from random import randrange
import LogoExtractor
from VideoCreator import generate_one_video

diversity = 1000000
app = FastAPI()


def get_path(tag):
    return "resources/" + str(randrange(diversity)) + "_" + tag + ".png"


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
def read_request(im1: Optional[str] = "", im2: Optional[str] = "", im3: Optional[str] = "",
                 desc1: Optional[str] = "", desc2: Optional[str] = "", desc3: Optional[str] = "",
                 url: Optional[str] = ""):
    video_len = 4
    W = 720
    H = 1280

    # input_path = get_path("in")
    # inp = io.BytesIO(im1.encode('ISO-8859-1'))
    # imageFile = Image.open(inp)
    # imageFile.save(input_path)
    # imageFile.close()

    path_1 = generate_one_video(
        video_len,
        x1=0, y1=0, x2=W, y2=int(H / 3),  # text position
        x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
        text=desc1,  # text
        path_to_image="logos/0.png",  # path to image
        animation_type='wiggle',  # type of animation
        url='https://pythonist.ru'
    )

    return {"video": path_1}
