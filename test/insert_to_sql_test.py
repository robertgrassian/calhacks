import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mysql.connection import *

sqlCon = MySqlConnection()
