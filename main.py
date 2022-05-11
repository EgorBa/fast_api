import io
import os
from typing import Optional
from PIL import Image
from fastapi import FastAPI
from random import randrange

import ColorsGetter
import LogoExtractor
import server
from VideoCreator import generate_one_video
from moviepy.editor import *
import firebase_admin
from firebase_admin import db
import requests

cred_object = firebase_admin.credentials.Certificate('panelcreama-firebase-adminsdk-pxxap-8daf8c0b6c.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': 'https://panelcreama-default-rtdb.firebaseio.com'
})

diversity = 1000000
app = FastAPI()


def get_path(tag):
    return str(randrange(diversity)) + "_" + tag + ".png"


def get_path_video(tag):
    return str(randrange(diversity)) + "_" + tag + ".avi"


def get_colors_from_str(array):
    if array is None:
        return None
    strs = array[2:(len(array) - 2)].split("],[")
    mas1 = tuple(map(int, strs[0].split(',')))
    mas2 = tuple(map(int, strs[1].split(',')))
    return (mas1, mas2)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/logo/{item_id}")
def read_q(site: Optional[str] = "", logo_id: Optional[int] = 0):
    (rgb_colors, new_rgb_colors) = ((255, 0, 0), (0, 0, 0))
    if logo_id <= 0:
        im_url = LogoExtractor.get_icon(site)
        if im_url != "":
            p = requests.get(im_url)
            inp = io.BytesIO(p.content)
            image_file = Image.open(inp)
            logo_path = get_path("in")
            image_file.save(logo_path)
            (rgb_colors, new_rgb_colors) = ColorsGetter.get_colors_by_logo(logo_path)
    else:
        image = db.reference("/").child("logos").child(str(logo_id)).get("image")[0]['image']
        logo_path = get_path("in")
        inp = io.BytesIO(image.encode('ISO-8859-1'))
        image_file = Image.open(inp)
        image_file.save(logo_path)
        image_file.close()
        (rgb_colors, new_rgb_colors) = ColorsGetter.get_colors_by_logo(logo_path)
    return {"colors": (rgb_colors, new_rgb_colors)}


@app.get("/generate/{item_id}")
def read_request(item_id: int, id: Optional[int] = 0, colors: Optional[str] = None,
                 animation_type: Optional[str] = "simple",
                 clear_bg: Optional[bool] = False, sale: Optional[str] = "",
                 use_emotion=False):
    if id == 0:
        return {"": ""}

    image = db.reference("/").child("images").child(str(id)).get("image")[0]['image']
    descr = db.reference("/").child("images").child(str(id)).get("descr")[0]['descr']

    video_len = 4
    W = 720
    H = 1280
    input_path = ""

    if image != "":
        input_path = get_path("in")
        inp = io.BytesIO(image.encode('ISO-8859-1'))
        image_file = Image.open(inp)
        image_file.save(input_path)
        image_file.close()
        if clear_bg:
            output_path = get_path("out")
            server.process_request_by_input_output_path(input_path, output_path)
            input_path = output_path

    if item_id == 0:
        path = generate_one_video(
            video_len,
            x1=30, y1=0, x2=W - 30, y2=H,  # text position
            text=descr,  # text
            animation_type=animation_type,  # type of animation
            colors=get_colors_from_str(colors),  # main colors
        )
    else:
        path = generate_one_video(
            video_len,
            x1=30, y1=0, x2=W - 30, y2=int(H / 3),  # text position
            x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
            text=descr,  # text
            path_to_image=input_path,  # path to image
            animation_type=animation_type,  # type of animation
            colors=get_colors_from_str(colors),  # main colors
            x5=400, y5=400, x6=600, y6=600,  # promo coordinates
            promo_text=sale,  # promo text
            use_emotion=use_emotion,  # add emotion instead of empty image
        )

    if path != "":
        image_file_obj = open(path, 'rb')
        image_binary_bytes = image_file_obj.read()
        image_stream = io.BytesIO(image_binary_bytes)
        s = image_stream.read().decode('ISO-8859-1')
        db.reference("/").child("videos").child(str(id)).child("video").set(s)
        os.remove(path)

    if input_path != "":
        os.remove(input_path)

    return {"video": "generating"}


@app.get("/videos/{item_id}")
def read_request(id0: Optional[int] = 0, id1: Optional[int] = 0, id2: Optional[int] = 0, id3: Optional[int] = 0):
    v0 = db.reference("/").child("videos").child(str(id0)).get("video")[0]
    v1 = db.reference("/").child("videos").child(str(id1)).get("video")[0]
    v2 = db.reference("/").child("videos").child(str(id2)).get("video")[0]
    v3 = db.reference("/").child("videos").child(str(id3)).get("video")[0]
    videos = []

    if v0 is not None:
        input_path = get_path_video("in")
        out_file = open(input_path, "wb")
        out_file.write(v0["video"].encode('ISO-8859-1'))
        out_file.close()
        videos.append(input_path)

    if v1 is not None:
        input_path = get_path_video("in")
        out_file = open(input_path, "wb")
        out_file.write(v1["video"].encode('ISO-8859-1'))
        out_file.close()
        videos.append(input_path)

    if v2 is not None:
        input_path = get_path_video("in")
        out_file = open(input_path, "wb")
        out_file.write(v2["video"].encode('ISO-8859-1'))
        out_file.close()
        videos.append(input_path)

    if v3 is not None:
        input_path = get_path_video("in")
        out_file = open(input_path, "wb")
        out_file.write(v3["video"].encode('ISO-8859-1'))
        out_file.close()
        videos.append(input_path)

    video_len = 4
    clips = []
    for i in range(len(videos)):
        clip = VideoFileClip(videos[i])
        if i == 0:
            clips.append(clip.set_start(i * video_len).crossfadeout(1))
        else:
            if i == len(videos) - 1:
                clips.append(clip.set_start(i * video_len).crossfadein(1))
            else:
                clips.append(clip.set_start(i * video_len).crossfadeout(1).crossfadein(1))
    video = CompositeVideoClip(clips)
    path = "main_variant.mp4"
    video.write_videofile(path, fps=25)
    image_file_obj = open(path, 'rb')
    image_binary_bytes = image_file_obj.read()
    image_file_obj.close()
    image_stream = io.BytesIO(image_binary_bytes)
    s = image_stream.read().decode('ISO-8859-1')

    db.reference("/").child("videos").child(str(id0) + str(id1) + str(id2) + str(id3)).child("video").set(s)

    os.remove(path)
    for p in videos:
        os.remove(p)

    return {"video": "ready"}


@app.get("/mock/{item_id}")
def read_request(path: Optional[str] = ""):
    image_file_obj = open(path, 'rb')
    image_binary_bytes = image_file_obj.read()
    image_stream = io.BytesIO(image_binary_bytes)
    s = image_stream.read().decode('ISO-8859-1')
    return {"video": s}
