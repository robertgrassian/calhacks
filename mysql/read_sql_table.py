import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
import pandas as pd

def read_sql_table(tableName):
    engine = create_engine("mysql+mysqldb://server:calhacks@localhost:3306/face_base")
    df = pd.read_sql_table(table_name=tableName, con=engine)
    return df
