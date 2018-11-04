import requests
import datetime
import time
import cv2
import os


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
            raise Exception('Error: img parameter must be of type string')

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
        if len(self.seen) == 0:
            return None
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
        if len(recognized) == 0:
            return None
        if not isinstance(recognized, list):
            print("hmmmmmmm")
            print(recognized)
            return recognized
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
            print("deleting...")
            print(recognized_face)
            recognized_id = recognized_face['faceId']
            ids.append(recognized_id)
            if recognized_id in self.seen:
                self.remove_id(recognized_id)
            if curr_id in self.seen:
                self.remove_id(curr_id)
        return ids





class IN(System):
    def run(self, duration):  # TODO: Get rid of start_time if not using pseudosystem
        """Continuously takes in image frames and runs detection, logging them in set"""
        # for img in test_input:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Error: Video Camera not found")
        start_time = time.process_time()
        while True:
            if time.process_time() - start_time >= duration:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()
            cv2.imwrite('photo.jpg', frame)
            faces = self.detect('photo.jpg')
            os.remove('photo.jpg')
            self.log_faces(faces)
            # TODO: Send faces to database
        cap.release()


class OUT(System):
    def run(self, duration):  # TODO: Get ride of start_time if not using pseudosystem
        """Detects faces from input, runs detection to delete id from database and log output time"""
        # for img in test_input:
        cap = cv2.VideoCapture(0)
        start_time = time.process_time()
        while True:
            if time.process_time() - start_time >= duration:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()
            cv2.imwrite('photo.jpg', frame)
            faces = self.detect('photo.jpg')
            os.remove('photo.jpg')
            # For every face in frame, remove from list of current people
            removed_ids = self.remove_faces(faces)
            # Send leave time to database
            curr_time = self.time.today()
            output_data = []
            for curr_id in removed_ids:
                output_data.append({curr_id: curr_time})
            # TODO: Send output_data to database

        cap.release()


def run_system(subscription_key):
    """Runs Pseudosystem that imitates 2 webcams, switches between the 2 systems every 10 seconds"""
    in_system = IN(subscription_key)
    out_system = OUT(subscription_key)
    for _ in range(1):
        in_system.run(5)
        out_system.run(5)


def test():
    # sys = IN("553c3c0a400a4f6ea90223e6ae996ce3")
    # sys2 = OUT("553c3c0a400a4f6ea90223e6ae996ce3")
    # # 2 faces of 5 different people
    # in_input = ['orl_faces/s1/1.jpeg', 'orl_faces/s2/1.jpeg', 'orl_faces/s3/1.jpeg', 'orl_faces/s4/1.jpeg', 'orl_faces/s5/1.jpeg',
    #             'orl_faces/s1/2.jpeg', 'orl_faces/s2/2.jpeg', 'orl_faces/s3/2.jpeg', 'orl_faces/s4/2.jpeg', 'orl_faces/s5/2.jpeg']
    # out_input = ['orl_faces/s1/1.jpeg', 'orl_faces/s2/1.jpeg', 'orl_faces/s3/1.jpeg', 'orl_faces/s4/1.jpeg', 'orl_faces/s5/1.jpeg']
    # sys.run()
    # print(len(System.seen))
    # sys2.run(out_input)
    # print(len(System.seen))
    pass



run_system("553c3c0a400a4f6ea90223e6ae996ce3")
