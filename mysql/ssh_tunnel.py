from sshtunnel import SSHTunnelForwarder
import pandas as pd
from sqlalchemy import create_engine

private_key = '-----BEGIN RSA PRIVATE KEY-----MIIEowIBAAKCAQEAtsTT9pgvFsb7MPxLLyYzO9ZQ/gi2wZD7NYBjTEOuwldarJdCmPgdC9r8Olr5vFfq6BOQC72W39mUFxSgpP+nLtxJ6nhQoYF+E9qHUtW6LtKHvamy1Wz3o8mOGMNwEth96RIrSJu5BEj2rQecoHd9q69e+z0yaQkiIF1P+amuTGd/b4Hixj1mD0R1a0RznIdABOQ5fbEJe2J4KKb7lCiwlgUMim+86PRs0BE6O3OXgIAkFpaWtSZqlEhMHtd3PlxDEI/PKvlELC22CCiWnJkU1ekPrO8a+j6HAsSjmAepQhsvrrgnypiRfwNeH/EwlNSvqlpUtdZWN4T+ChMdlKZzAwIDAQABAoIBAAYIOwKxhSRYTuQP/58/wIMiEKxBt15uHYxnf19+AF+TqH93wo/v6G2Cvb5jUEjCEhO0yZVJnZgnwzZ7zM2FToxCYwIlFGwwLOwU01CNk0aGVkqRNkDLBuVV+qWglatZj9ZIbjtIQHP+wH13edjl+LTY5eae33IOBh1RVxljW0hUN9zS81vOLLRsQOUtxSJFUsIo/9VIIAogiV9GW44Kpc4y9mzk2MHtyYdGC1bt93hP7Vd3hQBJrPeWgKRfCoGj5CGwwIlBCMC/RPk8pRVxImwSzFKWXW599jd6DxKNOZTQnQbkU/7JiGxo49pEeQ+84+0MQ8nT1roRlZ7EXslmvukCgYEA3nPBwirTSvu0w79xi9DGFAPBbHdIPmt37nxhEFeKXu3xVjKCFjkBUfD2OM5cvr5UPWYCubFoKJ0WVLvyHqKkOQuy2qP+HTgc3QOxbHOhYX/nTTj/ZD9RytlbkI32BLD44nPUtvaxh8K6eHUg22oIxFUAUBY7cVLc5lXIfGM9lFcCgYEA0lUC+dDY8Xag76M5Pqm7mxTuBAbE8/ucAojqzm3yuTwMEE9Bmv8us4qIaRuByqQuTyZbPBNneVL7fwj791vhBEToDbxo3ZmFskF2iPOQZLll9Wr6e1VUkOkcjXauzSheFth+f31xA5Z+IB2UK3tId7Vuv9lJoze0UeSUxaxRCzUCgYBC9nWNDXctSzfO9QIpJF98BuVi0UVeBNvFXouZb8CnctkDKZEfP2m2UOLNltE0WfbhxKNtYooIL8FZIHpx3mOxCGR+jH8iLJIDtejizKv3vZjTFiVK+ASXG3cEvLciEmPZRyTxLrGiPGwFdry9T93zu+KsOQULx/XXIFuJlhYjYQKBgGp6INSItpqefGB0F/GyCUg78zZUmvYMpPDfkUbJgDvnuw+yn7qwflrjwaS8CRulu8/T0hH6nMJdkPXBfZS+jY4UuAjkHY45PuZ7n187NhjXhlcUPhObogDuEcdHkrxHOEKGfJtbzI+NavIlJzJP6eK4FYXHoTCgbYebmPjs/+YVAoGBAILRLRskNw9m82pCONjAuMCr6kWtYfjfTKgGBwAo5o//0Vb4DluExgIi4pSTYT4FCf7e8VqRfjwcdTWxOo+V+rSAw3cyZuTHfNz38qYAQeZBRTLO8OfAm4weuSmP8xkgGiHa4DST7uYc7jA7FjKkxS+03qQSMCCcNsG2xOzmQpte-----END RSA PRIVATE KEY-----'
def query(private_key):
    with SSHTunnelForwarder(
        ("18.223.212.152", 22),
        ssh_username='ec2-user',
        ssh_private_key='~/.ssh/calhacks.pem',
        remote_bind_address=('127.0.0.1', 3306),
    ) as server:
        conn = create_engine("mysql+mysqldb://server:calhacks@localhost:3306/face_base")
    df = pd.read_sql_table(table_name='testEnter', con=conn)
    print(df)

query(private_key)