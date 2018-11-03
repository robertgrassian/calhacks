import requests
import json

class System:
    def __init__(self, sub_key):
        self. subscription_key = sub_key
        assert self.subscription_key
        self.seen = set()

    def detect(self, img, file_type='url'):
        """Detects faces in img, img must be of type url or binary_data"""
        if not isinstance(img, str):
            raise Exception('Error: img_url parameter must be of type string')

        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,emotion,accessories'
        }
        if file_type == "binary_data":
            headers = {'Ocp-Apim-Subscription-Key': self.subscription_key,
                       'Content-Type': 'application/octet-stream'}
            f = open(img, "rb").read()
            response = requests.post(face_api_url, params=params, headers=headers, data=f)
        else:
            headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
            data = {'url': img}
            response = requests.post(face_api_url, params=params, headers=headers, json=data)

        faces = response.json()
        for face in faces:
            self.add_id(face['faceId'])
        return faces

    def recognizer(self, id, remove=False):
        """Returns json file of maxNumOdCandidatesReturned faces that match id1, each with confidence level
            Deletes id1 and matched face from self.seen"""
        if not isinstance(id, str):
            raise Exception('Error: id parameter must be of type string')
        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars'
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        data = {
            'faceId': id,
            'faceIds': self.seen,
            'mode': 'matchPerson',
            'maxNumOfCandidatesReturned': 1
        }
        response = requests.post(face_api_url, json=data, headers=headers)
        recognized = response.json()
        if remove:
            if id in self.seen:
                self.remove_id(id)
            for face in recognized:
                self.remove_id(face['faceId'])
        return recognized

    def get_ids(self):
        return self.seen

    def remove_id(self, id):
        self.seen.remove(id)

    def add_id(self, id):
        self.seen.add(id)





def test():
    sys = System("553c3c0a400a4f6ea90223e6ae996ce3")
    sys.detect('orl_faces/s1/1.jpg', 'binary_data')
    # sys.detect('https://how-old.net/Images/faces2/main007.jpg')



test()
