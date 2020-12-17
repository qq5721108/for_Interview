import mysql.connector
from sql_creat_queries import student_inf_query, student_avg_score_query, student_warn_score_query

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

    #print("查询快要被开除学生学号：")

    message = input("查询快要被开除学生学号:")
    
    while(message != 'q'):
        
        #query = "SELECT distinct * from student_teacher_view WHERE `sname` = '{}'".format(message)
        query = student_warn_score_query
        #query = student_avg_score_query.format(message)
        cur.execute(query)

        rows = cur.fetchall()
        index = cur.description
        col = []
        for i in index:
            col.append(i[0])

        for row in rows:
            #infor = {'id':row[0], '姓名':row[1], '出生日期':str(row[2]), '性别':row[3], '班级':row[4]}
            infor = zip(col, row)
            pri = []
            for i in (infor):
                pri.append([i[0], i[1]])
            print(pri)
        print()

        message = input("输入学生姓名(输入'q'退出):")

    
    conn.close()


if __name__ == "__main__":
    main()