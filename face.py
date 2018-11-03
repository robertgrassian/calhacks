import requests
import datetime

class System:
    CONFIDENCE = 0.5

    def __init__(self, sub_key):
        self. subscription_key = sub_key
        assert self.subscription_key
        self.seen = []
        self.time = datetime.datetime

    def detect(self, img, file_type='binary_data', add=True):
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
        # if add:
        #     for face in faces:
        #         if len(self.seen) != 0:
        #             cur_id = face['faceId']
        #             resp = self.recognizer(cur_id)
        #             if resp is None:
        #                 self.add_id(face['faceId'])
        #                 face['time'] = self.time.today()
        #                 continue
        #             # if confident that face is already logged, don't re-log it
        #             if resp['confidence'] >= System.CONFIDENCE:
        #                 continue
        #         self.add_id(face['faceId'])
        #         face['time'] = self.time.today()
        return faces

    def recognizer(self, cur_id, remove=False):
        """Returns json file of maxNumOdCandidatesReturned faces that match id1, each with confidence level
            Deletes id1 and matched face from self.seen"""
        if not isinstance(cur_id, str):
            raise Exception('Error: id parameter must be of type string')
        face_api_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/findsimilars'
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        data = {
            'faceId': cur_id,
            'faceIds': self.seen,
            'mode': 'matchPerson',
            'maxNumOfCandidatesReturned': 1
        }
        response = requests.post(face_api_url, json=data, headers=headers)
        recognized = response.json()
        if remove:
            if cur_id in self.seen:
                self.remove_id(cur_id)
            for face in recognized:
                self.remove_id(face['faceId'])
        if len(recognized) == 0:
            return None
        return recognized[0]

    def get_ids(self):
        return self.seen

    def remove_id(self, id):
        self.seen.remove(id)

    def add_id(self, id):
        self.seen.append(id)

    def log_faces(self, faces):
        """Adds faces to self.seen if they are new"""
        for face in faces:
            if len(self.seen) != 0:
                cur_id = face['faceId']
                resp = self.recognizer(cur_id)
                if resp is None:
                    self.add_id(face['faceId'])
                    face['time'] = self.time.today()
                    continue
                # if confident that face is already logged, don't re-log it
                if resp['confidence'] >= System.CONFIDENCE:
                    continue
            self.add_id(face['faceId'])
            face['time'] = self.time.today()


class IN(System):
    def run(self):
        """Continuously takes in image frames and runs detection, logging them in set"""
        on = True
        while on:
            #TODO: Get images from a webcam continuously
            curr_image = 'orl_faces/s1/1.jpeg' #for now
            faces = self.detect(curr_image)
            self.log_faces(faces)
            #TODO: Send data to database


class OUT(System):
    def run(self):
        """Detects faces from input, runs detection to delete id from database and log output time"""
        pass


def test():

    sys = IN("553c3c0a400a4f6ea90223e6ae996ce3")
    sys.log_faces(sys.detect('orl_faces/s1/1.jpeg'))
    sys.log_faces(sys.detect('orl_faces/s1/2.jpeg'))
    sys.log_faces(sys.detect('orl_faces/s1/3.jpeg'))
    sys.log_faces(sys.detect('orl_faces/s2/1.jpeg'))
    sys.log_faces(sys.detect('orl_faces/s2/2.jpeg'))
    print(len(sys.seen))
    # r = r[0]
    # print(r['faceId'])
    # t =sys.recognizer(r['faceId'])
    # print(t)




test()
