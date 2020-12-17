import mysql.connector
from sql_creat_queries import create_table_queries, drop_table_queries, create_index_queries, creat_view_queries
from mysql.connector import errorcode
from pandas import DataFrame as df
import pandas
import sys

def exe_sql_queries(query, cur, connect):
    try:
        cur.execute(query)
    except ValueError as v:
        print(v)
    except :
        print ("不明错误", sys.exc_info()[0])
    else:
        connect.commit()
        print("插入成功") 
    


def insert_student_data(data, cur, connect):
    """
    向数据库中插入学生信息
    Parm: data, DataFrame, 学生信息
        cur, 游标
        connect,链接
    Return: null
    """
    values = ['3051009', 'HA2113002', 70]
    #print(data.values)
    query = "INSERT students (id, name, gender, class_id, birthday) values ('{}', '{}', '{}', '{}', '{}')".format(*values)
    exe_sql_queries(query, cur, connect)

def insert_course_sort_data(data, cur, connect):
    query = "INSERT course_sort (name, credit) values ('{}', '{}')".format(*data.values)
    exe_sql_queries(query, cur, connect)

def insert_course_data(data, cur, connect):
    query = "INSERT courses (course_id, class_id, course_name, teacher_id, major_id) values ('{}', '{}', '{}', '{}', '{}')".format(*data.values)
    exe_sql_queries(query, cur, connect)
    
def insert_score_data(data, cur, connect):
    #values = ['3051009', 'HA2113002', 70]
    #print(*data.values)
    query = "INSERT score (student_id, course_id, score) values ('{}', '{}', '{}')".format(*data.values)
    exe_sql_queries(query, cur, connect)

def insert_plan_data(data, cur, connect):
    #values = ['3051009', 'HA2113002', 70]
    #print(*data.values)
    query = "INSERT plan_details (course_name, course_type, major_id) values ('{}', '{}', '{}')".format(*data.values)
    exe_sql_queries(query, cur, connect)

def main():
    """
    Driver main function.
    """
    config = {
        'host' : "59.110.229.244",
        'user' : 'root',
        'password' : 'Qwe1336567',
        'auth_plugin' :'mysql_native_password',
        'use_pure' : 'True'
    }
    
    conn = mysql.connector.connect(**config, database = 'modeldb')
    cur = conn.cursor()

    road = "C:\\Users\\Trine\\Documents\\Tencent Files\\649466481\\FileRecv\\数据\\courses1.csv"
    
    with open(road,  encoding='UTF-8') as f:
        file = pandas.read_csv(f)
        print(file.head())

        for i, value in file.iterrows():
            #insert_student_data(value, cur, conn)
            insert_plan_data(value, cur, conn)
    """
    rows = cur.fetchall()

    for row in rows:
        print(row)
"""
    
    conn.close()


if __name__ == "__main__":
    main()