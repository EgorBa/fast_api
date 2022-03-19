import io

imageFileObj = open("logos/0.png", 'rb')
imageBinaryBytes = imageFileObj.read()
imageStream = io.BytesIO(imageBinaryBytes)
s = imageStream.read().decode('ISO-8859-1')

print(s)
