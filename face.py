import requests


class System:
    def __init__(self, sub_key):
        self. subscription_key = sub_key
        assert self.subscription_key
        self.seen = []

    def detect(self, img_url):
        if not isinstance(img_url, str):
            raise Exception('Error: img_url parameter must be of type string')
        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,emotion,accessories'
        }
        data = {'url': img_url}
        response = requests.post(face_api_url, params=params, headers=headers, json=data)
        faces = response.json()
        for face in faces:
            self.seen.append(self.get_attribute(face, 'faceId'))

        return faces

    def recognizer(self, id1, remove=False):
        """Returns json file of maxNumOdCandidatesReturned faces that match id1, each with confidence level
            Deletes id1 and matched face from self.seen"""
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
        if remove:
            self.remove_id(id1)
            for face in recognized:
                self.remove_id(self.get_attribute(face, 'faceId'))

        return recognized

    def get_ids(self):
        return self.seen

    def remove_id(self, id):
        self.seen.remove(id)

    def get_attribute(self, data, attr):
        return data[attr]




def test():
    sys = System("553c3c0a400a4f6ea90223e6ae996ce3")
    sys.detect('https://how-old.net/Images/faces2/main007.jpg')
    sys.recognizer(sys.seen[0], False)

test()
