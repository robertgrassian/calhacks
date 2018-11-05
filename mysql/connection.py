import MySQLdb
from mysql.constants import *

class MySqlConnection():
    def __init__(self):
        print("Open MySQLConnection...")
        self.connection = MySQLdb.connect(host="<serverip>", port=3306, user='server', passwd='', db='face_base')
        if (self.connection):
            print("Conn Success")
        else:
            print("Conn not success")
        print("MySQLConnection opened successfully!")
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

    def __del__(self):
        print("Close MySQLConnection...")
        self.connection.close()


def queryExecute(commandType, inputSql, param):
    # type: '1' (SELECT), '2'(INSERT),  '3'(UPDATE), '4'(DELETE)
    # create connection
    con = MySqlConnection()

    try:
        # execute query
        if isinstance(param, list):
            con.cursor.executemany(inputSql, param)
        else:
            con.cursor.execute(inputSql, param)
    except MySQLdb.Error as e:
        print('************************')
        print('MySQLdb.Error: ', e)
        print('************************')
    
    print("sql(execute): " + str(con.cursor._last_executed))

    if commandType == STR_SQLTYPE_SELECT:
        msg = 'result'
        for row in con.cursor:
            print(msg + "      :" + str(row))
            msg = '       '
    print("______________________________")

    # Commit
    con.connection.commit()

    if commandType == STR_SQLTYPE_INSERT:
        sql = ("SELECT LAST_INSERT_ID()")
        con.cursor.execute(sql)
    return con.cursor
