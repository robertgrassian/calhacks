import requests
import datetime
import time
import cv2
import os
import threading


class System:
    CONFIDENCE = 0.5
    seen = []
    curr_data = {}
    all_data = {}
    left_data = {}
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
            if 'mask' in face['faceAttributes']['accessories']:
                face['faceAttributes']['accessories'] = True
            else:
                face['faceAttributes']['accessories'] = False
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
            raise Exception("Probably Error with the recognizer")
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
            cur_id = face['faceId']
            if len(self.seen) != 0:
                resp = self.recognizer(cur_id)
                if resp is None:
                    self.add_id(cur_id)
                    System.curr_data[cur_id] = face
                    System.all_data[cur_id] = face
                    continue
                # if confident that face is already logged, don't re-log it
                if resp['confidence'] >= System.CONFIDENCE:
                    continue
            self.add_id(cur_id)
            System.curr_data[cur_id] = face
            System.all_data[cur_id] = face

    def remove_faces(self, faces):
        """Removes all matching faces from self.seen, returns list of ids that were deleted"""
        ids = []  # Consists of sublists [old_id, recognized_id]
        for face in faces:
            curr_id = face['faceId']
            recognized_face = self.recognizer(curr_id)
            if recognized_face is None:
                continue  # Person left who was not recorded entering...
            # If not confident that person is a match, don't remove
            if recognized_face['confidence'] < System.CONFIDENCE:
                continue
            recognized_id = recognized_face['faceId']
            ids.append([curr_id, recognized_id])
            if recognized_id in self.seen:
                self.remove_id(recognized_id)
                del System.curr_data[recognized_id]
            if curr_id in self.seen:
                self.remove_id(curr_id)
                del System.curr_data[curr_id]
        return ids





class IN(System):
    def run(self):  # TODO: Get rid of start_time if not using pseudosystem
        """Continuously takes in image frames and runs detection, logging them in set"""
        # for img in test_input:
        print("starting in")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Error: IN video Camera not found")
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()
            cv2.imwrite('photo1.jpg', frame)
            faces = self.detect('photo1.jpg')
            os.remove('photo1.jpg')
            self.log_faces(faces)
            print("Faces currently inside ", self.seen)
            # TODO: Send faces to database
        cap.release()


class OUT(System):
    def run(self):  # TODO: Get ride of start_time if not using pseudosystem
        """Detects faces from input, runs detection to delete id from database and log output time"""
        # for img in test_input:
        print("starting out")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            raise Exception("Error: OUT video camera not found")
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()
            cv2.imwrite('photo2.jpg', frame)
            faces = self.detect('photo2.jpg')

            os.remove('photo2.jpg')
            # For every face in frame, remove from list of current people
            removed_ids = self.remove_faces(faces)
            for old_id, matched_id in removed_ids:
                for face in faces:
                    if face['faceId'] == old_id:
                        System.left_data[matched_id] = face
                        System.left_data[matched_id]['faceId'] = matched_id

            print("Faces left", System.left_data)


            # curr_time = self.time.today()
            # output_data = []
            # for curr_id in removed_ids:
            #     output_data.append({curr_id: curr_time, })
            # TODO: Send output_data to database

        cap.release()


def run_system(subscription_key):
    """Runs Pseudosystem that imitates 2 webcams, switches between the 2 systems every 10 seconds"""
    in_system = IN(subscription_key)
    out_system = OUT(subscription_key)

    t1 = threading.Thread(name='in', target=in_system.run)
    t2 = threading.Thread(name='out', target=out_system.run)
    t1.start()
    t2.start()
    # Call graph func


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
