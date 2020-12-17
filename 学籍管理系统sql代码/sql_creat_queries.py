# DROP TABLES
class_table_drop = "DROP TABLE IF EXISTS  classes"
course_sort_table_drop = "DROP TABLE IF EXISTS  course_sort"
#students_table_drop = "DROP TABLE IF EXISTS  students"
#teacher_table_drop = "DROP TABLE IF EXISTS  teachers"
plan_detail_table_drop = "DROP TABLE IF EXISTS plan_details"
plan_table_drop = "DROP TABLE IF EXISTS plan"
"""



plan_detail_table_drop = "DROP TABLE IF EXISTS plan_details"
major_table_drop = "DROP TABLE IF EXISTS majors"
"""
# CREATE TABLES

	students_table_create = ("""CREATE TABLE IF NOT EXISTS students(
		`id` INT(10)  PRIMARY KEY AUTO_INCREMENT,
		`name` VARCHAR(5) NOT NULL DEFAULT '',
		`birthday` DATE   DEFAULT '1000-10-10',
		`gender` CHAR(1)  CHECK((`gender` = '男') or (`gender` = '女')) DEFAULT '男',
		`class_id` INT(10) REFERENCES classes(`id`)
	)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

#`class_id` VARCHAR(15) NOT NULL REFERENCES classes('id')
class_table_create = ("""CREATE TABLE IF NOT EXISTS  classes(
	`id` INT(10) PRIMARY KEY AUTO_INCREMENT,
	`class_name` Varchar(10) ,
	`major_id` INT(10)  REFERENCES majors(`id`)
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")


score_table_create = ("""CREATE TABLE  IF NOT EXISTS score(
	`id` INT(10)  NOT NULL AUTO_INCREMENT,
	`student_id` INT(10) REFERENCES students(`id`),
	`course_id` Char(8)  REFERENCES courses(`course_id`),
	`score` tinyint(3)  CHECK(score >=0 or score <= 100 or score is NULL) ,
	`is_make_up` tinyint(1)  CHECK(is_make_up = 0 or is_make_up = 1),
	PRIMARY KEY(`id`, `student_id`, `course_id`)
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

courses_table_create = ("""CREATE TABLE IF NOT EXISTS  courses(
	`course_id`  Char(8) PRIMARY KEY  ,
	`class_id` INT(10) REFERENCES classes(`id`),
	`course_name`  VARCHAR(10)  REFERENCES course_sort(`name`), 
	`teacher_id` INT(10) REFERENCES teachers(`id`),
	`class_time` DATE  DEFAULT '1000-10-10'
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

teachers_table_create = ("""CREATE TABLE IF NOT EXISTS  teachers(
	`id` INT(10) PRIMARY KEY AUTO_INCREMENT ,
	`name` Varchar(10) NOT NULL DEFAULT '',
	`gender` CHAR(1) CHECK((`gender` = '男') or (`gender` = '女')) DEFAULT '男',
	`birthday` DATE DEFAULT '1000-10-10',
	`college_id` Varchar(10) REFERENCES colleges(`name`)
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

plan_detail_table_create = ("""CREATE TABLE IF NOT EXISTS  plan_detials(
	`id` INT(10) PRIMARY KEY AUTO_INCREMENT ,
	`course_name` VARCHAR(20) NOT NULL REFERENCES course_sort(`name`) ,
	`course_type` CHAR(2) NOT NULL DEFAULT '选修',
	`semester` CHAR(3) NOT NULL DEFAULT '大一上',
	`major_id` INT(10)  REFERENCES majors(`id`)
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

major_table_creat = ("""CREATE TABLE IF NOT EXISTS  majors(
	`id` INT(10) PRIMARY KEY AUTO_INCREMENT ,
	`name` VARCHAR(10) NOT NULL,
	`college_name` VARCHAR(10)  REFERENCES colleges(`name`)
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

course_sort_create = ("""CREATE TABLE  IF NOT EXISTS course_sort(
	`name` VARCHAR(20) PRIMARY KEY ,
	`credit`  TINYINT(10) NOT NULL CHECK(credit > 0) DEFAULT '0'
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")

colleges_create = ("""CREATE TABLE  IF NOT EXISTS colleges(
	`name` VARCHAR(10) PRIMARY KEY  
)ENGINE=InnoDB  DEFAULT CHARSET=UTF8""")


# CREATE VIEW
view_student_score_information_create = ("""CREATE VIEW student_score_view AS(
	SELECT DISTINCT s.id, s.name , sc.score, cos.name as course_name, cos.credit, 
	cs.course_id,  pd.course_type, pd.semester,
	CASE 
	WHEN sc.score < 60 THEN 'fall'
	WHEN sc.score >= 60 THEN 'pass'
	END is_pass
	FROM students s INNER JOIN
	score sc ON s.id = sc.student_id
	INNER JOIN courses cs 
	ON cs.course_id = sc.course_id
	INNER JOIN course_sort cos
	ON cos.name = cs.course_name 
	INNER JOIN classes cl
	ON cl.id = s.class_id 
	INNER JOIN plan_details pd
	ON pd.major_id = cl.major_id AND pd.course_name = cs.course_name
	)""")

view_student_teacher_information_create = ("""CREATE VIEW student_teacher_view AS(
	SELECT s.name AS sname, t.name AS tname FROM students s INNER JOIN 
	courses cs ON s.class_id = cs.class_id INNER JOIN
	teachers t ON cs.teacher_id = t.id)""")

view_student_dropout_information_create = ("""CREATE VIEW student_dropout_view AS(
	SELECT s.name , sc.score, cos.name as course_name, cos.credit, cs.course_id,
	CASE 
	WHEN sc.score < 60 THEN 'fall'
	WHEN sc.score >= 60 THEN 'pass'
	END is_pass
	FROM students s INNER JOIN
	score sc ON s.id = sc.student_id
	INNER JOIN courses cs 
	ON cs.course_id = sc.course_id
	INNER JOIN course_sort cos
	ON cos.name = cs.course_name)""")

# QUERY LISTS

create_table_queries = [colleges_create, course_sort_create, plan_detail_table_create, major_table_creat, 
						teachers_table_create, class_table_create, courses_table_create, score_table_create, class_table_create,
						 students_table_create]

drop_table_queries = [class_table_drop, course_sort_table_drop, plan_table_drop]

create_index_queries = ["CREATE INDEX std_id_index ON students(`id`)",
            "CREATE INDEX score_id_index ON score(`id`)"]

creat_view_queries = [view_student_score_information_create,view_student_teacher_information_create,
					view_student_dropout_information_create]

student_inf_query = ("""SELECT students.`name` from students
                   INNER JOIN classes
                   ON classes.id = students.class_id
                   INNER JOIN majors
                   ON majors.id = classes.major_id
                   WHERE majors.`name` = '{}'""")

student_inf_query = ("""SELECT course_name, course_type, credit, semester, score
					FROM student_score_view
					WHERE id = {}""")

student_avg_score_query = ("""SELECT n1.*, n2.*
					FROM (SELECT  sum(credit*score)/SUM(credit) as avg_score_obligatory from student_score_view 
								GROUP BY id, course_type
								HAVING id = {} AND course_type = '必修') AS n1
					, (SELECT  sum(credit*score)/SUM(credit) as avg_score_all from student_score_view 
								GROUP BY id
								HAVING id = {} ) AS n2""")

student_warn_score_query = ("""SELECT id from 	
	(SELECT n1.id ,
		CASE 
			WHEN n1.s1 >= 7 AND n1.s1 < 10 THEN 'warn'
			ELSE 'good'
		END  ob,
		CASE 
		WHEN n2.s2 >= 12 AND n2.s2 < 115 THEN 'warn'
		ELSE 'good'
		END x
	FROM (SELECT  sum(credit) as s1, id
				from student_score_view 
				GROUP BY id, course_type, is_pass
				HAVING course_type = '必修' and is_pass = 'fall' ) AS n1 INNER JOIN
	 (SELECT  sum(credit) as s2, id 
				from student_score_view 
				GROUP BY id, course_type, is_pass
				HAVING course_type = '选修' and is_pass = 'fall' ) AS n2
	ON n1.id = n2.id) totle
WHERE totle.ob = 'warn' or totle.x = 'warn'

""")

