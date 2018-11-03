import MySQLdb


class MySqlConnection():
    def __init__(self):
        print("Open MySQLConnection...")
        self.connection = MySQLdb.connect(host="18.223.212.152", port=3306, user='yoneo', passwd='raptor98', db='face_base', charset='utf8')
        self.cursor = self.connection.cursor(MySQLdb.cursor.DictCursor)

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

    if commandType == STR_SQLTYPE_SELECT