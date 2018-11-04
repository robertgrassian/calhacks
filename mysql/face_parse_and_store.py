import pandas as pd
import MySQLdb
from mysql.constants import *
from mysql.connection import *
from sqlalchemy import create_engine
# Takes a pandas dataframe and stores it in the SQL database. 
def store_to_db(dataframe, enterBool):
    # Uses Pandas to_sql method to write to our database. Makes our job very easy.
    # Establish connection to our server/ database
    #sqlConn = MySqlConnection()
    engine = create_engine("mysql+mysqldb://server:calhacks@localhost:3306/face_base")
    # Try to add row to table, otherwise creates the table
    # TODO Change the table name to the final one that we'll be using

    if (enterBool):
        try:
            dataframe.to_sql(name='testEnter', con=engine, if_exists='replace')
        except ValueError as v:
            print("Value error, this shouldnt happen: " + v)
    else:
        try:
            dataframe.to_sql(name='testExit', con=sqlConn.connection, if_exists='append')
        except ValueError as v:
            print("Value error, this shouldnt happen: " + v)
