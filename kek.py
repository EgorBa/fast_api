import io
import json

import urllib.parse
import requests

import firebase_admin
from firebase_admin import db

imageFileObj = open("logos/0.png", 'rb')
imageBinaryBytes = imageFileObj.read()
imageStream = io.BytesIO(imageBinaryBytes)
s = imageStream.read().decode('ISO-8859-1')
print(len(s))

cred_object = firebase_admin.credentials.Certificate('panelcreama-firebase-adminsdk-pxxap-8daf8c0b6c.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': 'https://panelcreama-default-rtdb.firebaseio.com'
})

# db.reference("/").child("Books").set({
#     "Books":
#         {
#             "Best_Sellers": s
#         }
# })

print(db.reference("/").child("Books").child("Books").get("Best_Sellers")[0]['Best_Sellers'])

# imageFileObj = open("logos/1.png", 'rb')
# imageBinaryBytes = imageFileObj.read()
# imageStream = io.BytesIO(imageBinaryBytes)
# s = imageStream.read().decode('ISO-8859-1')
# print(len(s))
# p = requests.get(
#     "https://afternoon-waters-50114.herokuapp.com/create/1?desc1=kek&im1=" + urllib.parse.quote(s))
# print("--------------------")
# print(p.json()['video'])
# out_file = open("videos/3.avi", "wb")
# out_file.write(p.json()['video'].encode('ISO-8859-1'))
# out_file.close()

# h = open("samplefile.avi", 'rb')
# p = h.read()
# print(p)
# print(len(p))
