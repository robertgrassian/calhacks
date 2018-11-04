import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_handler import *


print("Reading in sql data...")
testJson = testJson = {  
      'faceId':"a5454d67-b57e-4bd0-bef4-fd3970aacc47",
      "faceRectangle":{  
         "top":29,
         "left":4,
         "width":79,
         "height":79
      },
      "faceAttributes":{  
         "gender":"male",
         "age":27.0,
         "emotion":{  
            "anger":0.0,
            "contempt":0.0,
            "disgust":0.0,
            "fear":0.0,
            "happiness":0.0,
            "neutral":0.975,
            "sadness":0.025,
            "surprise":0.0
         },
         "accessories": {
            "glasses": True
         },
      },
      "time":"2018"
   }
data_in(testJson)
print("All tests work")