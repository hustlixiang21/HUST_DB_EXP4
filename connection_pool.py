import psycopg2
from psycopg2 import pool
from psycopg2.extensions import connection

# 创建连接池
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # 最小和最大连接数
    dbname="s_t_u202112149",
    user="gaussdb",
    password="Lixiang@123",
    host="127.0.0.1",
    port="5432"
)


def get_connection() -> connection:
    """
    获取一个数据库连接
    :return: 数据库连接
    """
    return connection_pool.getconn()


def release_connection(conn):
    """
    释放一个数据库连接
    :param conn: 要释放的连接
    """
    connection_pool.putconn(conn)


def close_all_connections():
    """
    关闭所有连接
    """
    connection_pool.closeall()
