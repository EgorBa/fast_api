import os
import cv2
import numpy as np
import io
from rembg.bg import remove
from PIL import Image, ImageFile
from random import randrange
import threading

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
ImageFile.LOAD_TRUNCATED_IMAGES = True

diversity = 1000000


def process_request_by_input_output_path(input_path, output_path):
    print("Process img : " + input_path)
    try:
        if contains_white_bg(input_path):
            use_cv_and_rembg(input_path, output_path)
        else:
            use_rembg(input_path, output_path)
    except Exception:
        result_str = 'Something went wrong'


def clean(path):
    th = threading.Thread(target=os.remove, args=(path,))
    th.start()


def use_cv_and_rembg(input_path, output_path):
    output_path_cv2 = get_path("output_cv2")
    output_path_rembg = get_path("output_rembg")

    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
    mask = 255 - mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.GaussianBlur(mask, (0, 0), sigmaX=2, sigmaY=2, borderType=cv2.BORDER_DEFAULT)
    mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask
    cv2.imwrite(output_path_cv2, result)

    f = np.fromfile(input_path)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(output_path_rembg)

    img1 = Image.open(output_path_cv2)
    img2 = Image.open(output_path_rembg)
    img1.paste(img2, (0, 0), mask=img2)
    img1.save(output_path)
    img1.close()
    img2.close()

    clean(output_path_rembg)
    clean(output_path_cv2)


def use_rembg(input_path, output_path):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)
    output.close()


def contains_white_bg(path):
    image = Image.open(path)
    pix = image.load()
    a = pix[0, 0][0]
    b = pix[0, 0][1]
    c = pix[0, 0][2]
    if a + b + c > 750:
        return True
    return False


def get_path(tag):
    return str(randrange(diversity)) + "_" + tag + ".png"
