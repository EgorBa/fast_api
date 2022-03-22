import io

import requests

imageFileObj = open("logos/0.png", 'rb')
imageBinaryBytes = imageFileObj.read()
imageStream = io.BytesIO(imageBinaryBytes)
s = imageStream.read().decode('ISO-8859-1')

print(len(s))


# p = requests.get("https://afternoon-waters-50114.herokuapp.com/create/1?desc1=lol")
# print(p.json()['video'].encode('ISO-8859-1'))
# print(p.json()['video'])
# print(len(p.json()['video'].encode('UTF-8').decode('UTF-8').encode('ISO-8859-1')))
#
# out_file = open("videos/1.avi", "wb")
# out_file.write(p.json()['video'].encode('ISO-8859-1'))
# out_file.close()

# h = open("samplefile.avi", 'rb')
# p = h.read()
# print(p)
# print(len(p))
