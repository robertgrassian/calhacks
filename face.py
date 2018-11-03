import requests
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO


class System:
    def __init__(self, sub_key):
        self. subscription_key = sub_key
        assert self.subscription_key
        self.seen = []

    def detect(self, img_url):

        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }
        data = {'url': img_url}
        response = requests.post(face_api_url, params=params, headers=headers, json=data)
        faces = response.json()
        for face in faces:
            self.seen.append(face['faceId'])
        return faces

    def recognizer(self, id1):
        if not isinstance(id1, str):
            raise Exception('Error: id parameter must be of type string')
        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars'
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        data = {
            'faceId': id1,
            'faceIds': self.seen,
            'mode': 'matchPerson',
            'maxNumOfCandidatesReturned': 1
        }
        response = requests.post(face_api_url, json=data, headers=headers)
        recognized = response.json()
        return recognized






sys = System("553c3c0a400a4f6ea90223e6ae996ce3")
sys.detect('https://how-old.net/Images/faces2/main007.jpg')
sys.recognizer(sys.seen[0])

