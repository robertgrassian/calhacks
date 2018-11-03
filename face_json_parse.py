import json
import pandas as pd
import sys

# Receives face json file and parses it into tabular format.
# Cleans it up so we can store it in MySQL and use in Pandas. 
def to_normalized_dataframe(jsonIn):
    # Creates a dataframe of the normalized face JSON file.
    # Makes the nested data of the face data tabular & flat.
    try:
        normalized_json_dataframe = pd.io.json.json_normalize(jsonIn)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return normalized_json_dataframe
