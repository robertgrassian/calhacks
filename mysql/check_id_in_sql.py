import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine
import pandas as pd 

def id_check(json):
    engine = create_engine("mysql+mysqldb://root:raptor98@18.223.212.152:3306/face_base")
    df = pd.read_sql(name='testEnter', con=engine, if_exists='replace')

