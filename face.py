import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
subscription_key = "553c3c0a400a4f6ea90223e6ae996ce3"
assert subscription_key


def detect(img_url):

    face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    data = {'url': img_url}
    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    faces = response.json()




detect('https://how-old.net/Images/faces2/main007.jpg')