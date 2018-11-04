import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysql.connection import *
from parsing.face_json_parse import *
from mysql.face_parse_and_store import *
from datetime import datetime
# Instantiate example JSON file
# testJson = {  
#       'faceId':"a5454d67-b57e-4bd0-bef4-fd3970aacc47",
#       "faceRectangle":{  
#          "top":29,
#          "left":4,
#          "width":79,
#          "height":79
#       },
#       "faceAttributes":{  
#          "gender":"male",
#          "age":27.0,
#          "emotion":{  
#             "anger":0.0,
#             "contempt":0.0,
#             "disgust":0.0,
#             "fear":0.0,
#             "happiness":0.0,
#             "neutral":0.975,
#             "sadness":0.025,
#             "surprise":0.0
#          },
#          "accessories":[  
   
#          ]
#       },
#       "time":"2018"
#    }
testJson = {
    'firstname' : 'Yoneo',
    'lastname' : 'Arai',
    'age' : 20
}
print("test Json initialized")
# Parse JSON file to pandas dataframe
df = to_normalized_dataframe(testJson)
print("Test dataframe created")
# Append testJson to MySQL database
store_to_db(df, True)
print("Dataframe successfully pushed to sql")
