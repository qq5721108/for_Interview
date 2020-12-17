import mysql.connector
from sql_creat_queries import create_table_queries, drop_table_queries, create_index_queries, creat_view_queries
from mysql.connector import errorcode


def create_database():
    """

    返回数据库游标
    :return: 返回链接句柄与数据库游标
    """
    # connect to default database


    config = {
        'host' : "59.110.229.244",
        'user' : 'root',
        'password' : '***',
        'auth_plugin' :'mysql_native_password',
        'use_pure' : 'True'
    }
    #conn = mysql.connector.connect(**config)
    #conn.set_session(autocommit=True)
    #cur = conn.cursor()
    
    #cur.execute("DROP DATABASE IF EXISTS modeldb")
    #cur.execute("CREATE DATABASE IF NOT EXISTS modeldb CHARACTER SET utf8 COLLATE utf8_general_ci")

    # close connection to default database
    #conn.close()    
    
    # connect to modeldb database
    conn = mysql.connector.connect(**config, database = 'modeldb')
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    for query in drop_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    运行sql_creat_queries中的建表语句
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in create_table_queries:
        print(query)
        cur.execute(query)
        conn.commit()

def create_index(cur, conn):
    """
    运行sql_index_queries中的建表语句
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in create_index_queries:
        print(query)
        cur.execute(query)
        conn.commit()

def create_view(cur, conn):
    """
    运行sql_index_queries中的建表语句
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in creat_view_queries:
        print(query)
        cur.execute(query)
        conn.commit()
    

def main():
    """
    Driver main function.
    """
    cur, conn = create_database()
    
    #drop_tables(cur, conn)

    #create_tables(cur, conn)

    #create_index(cur, conn)

    create_view(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()