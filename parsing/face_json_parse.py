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
        for face in jsonIn:
            if normalized_json_dataframe:
                normalized_json_dataframe = pd.io.json.json_normalize(jsonIn)
            else:
                row = pd.io.json.json_normalize(jsonIn)
                normalized_json_dataframe = normalized_json_dataframe.append(row, ignore_index = True)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    return normalized_json_dataframe
