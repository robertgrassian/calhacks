import pandas as pd 
import numpy as np 
from parsing.face_json_parse import *
from mysql.face_parse_and_store import *
from mysql.read_sql_table import *

def data_in(jsonIn):
    # Creates df of newly imported data from Face API
    new_df = to_normalized_dataframe(jsonIn)
    # Catch if table doesn't exist
    try:
        old_sql = read_sql_table("testEnter").drop(['index'], axis=1)['faceId'].unique()
            # Check if ID already in database. If it is, 
        for id in new_df['faceId'].unique():
            if id in old_sql:
                new_df = new_df[new_df['faceId'] != id]

        # Appends new df to MySQL db
        store_to_db(new_df, True)
    except ValueError as e:
        print("Table doesn't exist, generating...")
        store_to_db(new_df, True)
        

    # Creates df based off of current SQL table TODO: Make sure table name is current
    current_data = read_sql_table("testEnter").drop(['index'], axis=1)
    return current_data
