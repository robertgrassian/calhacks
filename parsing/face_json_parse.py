import json
import pandas as pd
import sys

# Receives face json file and parses it into tabular format.
# Cleans it up so we can store it in MySQL and use in Pandas. 
def to_normalized_dataframe(jsonIn):
    normalized_json_dataframe = None
    # Creates a dataframe of the normalized face JSON file.
    # Makes the nested data of the face data tabular & flat.
    if type(jsonIn) is dict:
        try:
            normalized_json_dataframe = pd.io.json.json_normalize(jsonIn)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    elif type(jsonIn) is list:
        try:
            for face in jsonIn:
                if normalized_json_dataframe is None:
                    normalized_json_dataframe = pd.io.json.json_normalize(jsonIn)
                else:
                    row = pd.io.json.json_normalize(jsonIn)
                    normalized_json_dataframe = normalized_json_dataframe.append(row, ignore_index = True)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    return normalized_json_dataframe

def id_in_df(dataframe, id):
    ids = dataframe['faceId'].unique()
    if id in ids:
        return True
    return False

def df_append(dataframe, face_frame):
    if dataframe is None:
        return face_frame
    else:
        if not id_in_df(dataframe, face_frame['faceId'][0]):
            dataframe = dataframe.append(face_frame, ignore_index=True)
    return dataframe


