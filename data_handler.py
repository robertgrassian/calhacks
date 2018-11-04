import pandas as pd 
import numpy as np 
from parsing.face_json_parse import *
from mysql.face_parse_and_store import *
from mysql.read_sql_table import *

def data_in(jsonIn):
    # Creates df of newly imported data from Face API
    new_df = to_normalized_dataframe(jsonIn)

    # Appends new df to MySQL db
    store_to_db(new_df, True)

    # Creates df based off of current SQL table TODO: Make sure table name is current
    current_data = read_sql_table("testEnter").drop(['index'], axis=1)
    print(current_data)
    return current_data
