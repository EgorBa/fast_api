import io

import requests

imageFileObj = open("logos/0.png", 'rb')
imageBinaryBytes = imageFileObj.read()
imageStream = io.BytesIO(imageBinaryBytes)
s = imageStream.read().decode('ISO-8859-1')

print(len(s))
print("https://afternoon-waters-50114.herokuapp.com/create/1?desc1=kek&im1=" + str(s))
p = requests.get("https://afternoon-waters-50114.herokuapp.com/create/1?desc1=kek&im1=" + str(s))
print(p.json()['video'].encode('ISO-8859-1'))
out_file = open("videos/2.avi", "wb")
out_file.write(p.json()['video'].encode('ISO-8859-1'))
out_file.close()

# h = open("samplefile.avi", 'rb')
# p = h.read()
# print(p)
# print(len(p))
