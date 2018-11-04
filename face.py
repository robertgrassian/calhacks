import requests
import datetime


class System:
    CONFIDENCE = 0.5
    seen = []

    def __init__(self, sub_key):
        self.subscription_key = sub_key
        assert self.subscription_key
        self.time = datetime.datetime

    def detect(self, img, file_type='binary_data'):
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
        curr_time = self.time.today()
        for face in faces:
            face['time'] = curr_time
        return faces

    def recognizer(self, cur_id):
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
        # if remove:
            # if cur_id in self.seen:
            #     self.remove_id(cur_id)
            # for face in recognized:
            #     self.remove_id(face['faceId'])
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
                    continue
                # if confident that face is already logged, don't re-log it
                if resp['confidence'] >= System.CONFIDENCE:
                    continue
            self.add_id(face['faceId'])

    def remove_faces(self, faces):
        """Removes all matching faces from self.seen, returns list of ids that were deleted"""
        ids = []
        for face in faces:
            curr_id = face['faceId']
            recognized_face = self.recognizer(curr_id)
            if recognized_face is None:
                continue  # Person left who was not recorded entering...
            recognized_id = recognized_face['faceId']
            ids.append(recognized_id)
            if recognized_id in self.seen:
                self.remove_id(recognized_id)
            if curr_id in self.seen:
                self.remove_id(curr_id)
        return ids


class IN(System):
    def run(self, input):
        """Continuously takes in image frames and runs detection, logging them in set"""
        # TODO: Get images from a webcam continuously, remove input
        for img in input:
            faces = self.detect(img)
            self.log_faces(faces)
            # TODO: Send faces to database


class OUT(System):
    def run(self, input):
        """Detects faces from input, runs detection to delete id from database and log output time"""
        # TODO: Get images from webcam continuously, remove input
        for img in input:
            faces = self.detect(img)
            # For every face in frame, remove from list of current people
            removed_ids = self.remove_faces(faces)
            # Send leave time to database
            curr_time = self.time.today()
            output_data = []
            for curr_id in removed_ids:
                output_data.append({curr_id: curr_time})
            # TODO: Send output_data to database




def test():

    f = FrameGrabber()
    sys = IN("553c3c0a400a4f6ea90223e6ae996ce3")
    sys2 = OUT("553c3c0a400a4f6ea90223e6ae996ce3")
    # 2 faces of 5 different people
    in_input = ['orl_faces/s1/1.jpeg', 'orl_faces/s2/1.jpeg', 'orl_faces/s3/1.jpeg', 'orl_faces/s4/1.jpeg', 'orl_faces/s5/1.jpeg',
                'orl_faces/s1/2.jpeg', 'orl_faces/s2/2.jpeg', 'orl_faces/s3/2.jpeg', 'orl_faces/s4/2.jpeg', 'orl_faces/s5/2.jpeg']
    out_input = ['orl_faces/s1/1.jpeg', 'orl_faces/s2/1.jpeg', 'orl_faces/s3/1.jpeg', 'orl_faces/s4/1.jpeg', 'orl_faces/s5/1.jpeg']
    sys.run(in_input)
    print(len(System.seen))
    sys2.run(out_input)
    print(len(System.seen))




test()
