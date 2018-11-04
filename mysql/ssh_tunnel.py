from sshtunnel import SSHTunnelForwarder
import pandas as pd
from sqlalchemy import create_engine
def ssh_read_in_db():
    with SSHTunnelForwarder(
        ("18.223.212.152", 22),
        ssh_username='ec2-user',
        ssh_private_key='~/Desktop/calhacks.pem',
        remote_bind_address=('127.0.0.1', 3306),
    ) as server:
        conn = create_engine("mysql+mysqldb://server:calhacks@localhost:3306/face_base")
        conn.connect()
        df = pd.read_sql_table(table_name='testEnter', con=conn)
    print(df)

# def ssh_write_to_db():
#     with SSHTunnelForwarder(
#         ("18.223.212.152", 22),
#         ssh_username='ec2-user',
#         ssh_private_key='~/.ssh/calhacks.pem',
#         remote_bind_address=('127.0.0.1', 3306),
#     ) as server:
#         conn = create_engine("mysql+mysqldb://server:calhacks@localhost:3306/face_base")
#     dataframe.to_sql(name='testEnter', con=engine, if_exists='append')
#     print("Successfully wrote to MySQL...")


ssh_read_in_db()