import io
import json

import urllib.parse

import numpy as np
from urllib.parse import unquote
import requests
import numpy

# def get_colors_from_str(array):
#     if array is None:
#         return None
#     strs = array[2:(len(array) - 2)].split("],[")
#     mas1 = tuple(map(int, strs[0].split(',')))
#     mas2 = list(map(int, strs[1].split(',')))
#     return (mas1, mas2)

import firebase_admin
from firebase_admin import db

# imageFileObj = open("logos/0.png", 'rb')
# imageBinaryBytes = imageFileObj.read()
# imageStream = io.BytesIO(imageBinaryBytes)
# s = imageStream.read().decode('ISO-8859-1')
# print(len(s))
#
# cred_object = firebase_admin.credentials.Certificate('panelcreama-firebase-adminsdk-pxxap-8daf8c0b6c.json')
# default_app = firebase_admin.initialize_app(cred_object, {
#     'databaseURL': 'https://panelcreama-default-rtdb.firebaseio.com'
# })
# print(get_colors_from_str("[[1,1,1],[1,1,1]]"))

# db.reference("/").child("Books").set({
#     "Books":
#         {
#             "Best_Sellers": s
#         }
# })

# print(db.reference("/").child("Books").child("Books").get("Best_Sellers")[0]['Best_Sellers'])
# # print(db.reference("/").child("images").child(str(5316737)).get("image")[0]['image'])
# print(len(db.reference("/").child("videos").child(str(45944043118572451831)).get("video")[0]["video"].encode('ISO-8859-1')))

# imageFileObj = open("logos/1.png", 'rb')
# imageBinaryBytes = imageFileObj.read()
# imageStream = io.BytesIO(imageBinaryBytes)
# s = imageStream.read().decode('ISO-8859-1')
# print(len(s))
# p = requests.get(
#     "https://afternoon-waters-50114.herokuapp.com/videos/1?id0=5915764&id1=8920502&id2=8746451&id3=8361263")
# print("--------------------")
# out_file = open("videos/3.mp4", "wb")
# out_file.write(db.reference("/").child("videos").child(str(45944043118572451831)).get("video")[0]["video"].encode('ISO-8859-1'))
# out_file.close()
#
# print(np.multiply(np.array([2, 3]), np.array([2, 3])))

# h = open("samplefile.avi", 'rb')
# p = h.read()
# print(p)
# print(len(p))
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip

import server

# server.process_request_by_input_output_path("logos/img.png", "lol.png")
from VideoCreator import generate_one_video
#
video_len = 4
W = 720
H = 1280

# input_path = "logos/3.jpeg"
#
# output_path = "1.png"
# server.process_request_by_input_output_path(input_path, output_path)
# input_path = output_path

# path = generate_one_video(
#         video_len,
#         x1=30, y1=0, x2=W - 30, y2=int(H / 3),  # text position
#         x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
#         text="Удобные кросовки",  # text
#         path_to_image=input_path,  # path to image
#         animation_type="wiggle",  # type of animation
#         url="https://pythonist.ru/",
#         x5=400, y5=400, x6=600, y6=600,  # promo coordinates
#         promo_text="",  # promo text
# )

# path = generate_one_video(
#         video_len,
#         x1=30, y1=0, x2=W - 30, y2=int(H),  # text position
#         x3=0, y3=int(H / 3), x4=W, y4=H,  # image position
#         text="Pythonist.ru",  # text
#         path_to_image="",  # path to image
#         animation_type="scale",  # type of animation
#         url="https://pythonist.ru/",
#         x5=400, y5=400, x6=600, y6=600,  # promo coordinates
#         promo_text="",  # promo text
# )

videos = ["output_video_838756.avi", "output_video_850754.avi", "output_video_224366.avi", "output_video_721151.avi"]

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
