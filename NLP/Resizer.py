import os
from PIL import Image

W = float(720)
H = float(1280)

for im in os.listdir("faces"):
    path = "faces/" + im
    image = Image.open(path)
    (w, h) = image.size
    (w, h) = (float(w), float(h))
    d = w / h
    w = max(w, W)
    h = w / d
    h = max(h, H)
    w = d * h
    newsize = (int(w), int(h))
    image = image.resize(newsize)
    image.save(path)
