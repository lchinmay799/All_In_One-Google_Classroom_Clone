import sqlite3
from datetime import datetime
import sys

sys.path.insert(0, '/Desktop/myideas/Projects/Classroom_Clone/files')
import utilities as ut

def createTables(conn):
	conn.execute('''CREATE TABLE IF NOT EXISTS students(
		student_id INTEGER PRIMARY KEY AUTOINCREMENT,
		student_name VARCHAR(32),
		email VARCHAR(32),
		contact_number INTEGER,
		password VARCHAR(32),
		login_time DATETIME,
		logout_time DATETIME);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS teachers(
		teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
		teacher_name VARCHAR(32),
		email VARCHAR(32),
		contact_number INTEGER,
		password VARCHAR(32),
		login_time DATETIME,
		logout_time DATETIME);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS subjects(
		subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
		subject_name VARCHAR(32),
		subject_code VARCHAR(10));''')

	conn.execute('''CREATE TABLE IF NOT EXISTS handle(
		handle_id INTEGER PRIMARY KEY AUTOINCREMENT,
		teacher_id INTEGER NOT NULL,
		subject_id INTEGER NOT NULL,
		FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
		FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS enroll(
		enroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
		student_id INTEGER NOT NULL,
		subject_id INTEGER NOT NULL,
		FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
		FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS notes(
		notes_id INTEGER PRIMARY KEY AUTOINCREMENT,
		subject_id INTEGER NOT NULL,
		notes_sent DATETIME,
		notes_content VARCHAR(1000),
		FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS assignments(
		assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
		assignment_content VARCHAR(1000),
		assignment_assigned_date DATETIME,
		assignment_deadline DATETIME,
		subject_id INTEGER NOT NULL,
		FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS tests(
		test_id INTEGER PRIMARY KEY AUTOINCREMENT,
		test_content VARCHAR(1000),
		test_assigned_date DATETIME,
		test_deadline DATETIME,
		test_marks REAL,
		subject_id INTEGER NOT NULL,
		FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS assignmentSolutions(
		solution_id INTEGER PRIMARY KEY AUTOINCREMENT,
		student_id INTEGER NOT NULL,
		submitted_time DATETIME,
		assignment_id INTEGER NOT NULL,
		FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
		FOREIGN KEY(assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS testSolutions(
		solution_id INTEGER PRIMARY KEY AUTOINCREMENT,
		student_id INTEGER NOT NULL,
		submitted_time DATETIME,
		test_score REAL,
		test_id INTEGER NOT NULL,
		FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
		FOREIGN KEY(test_id) REFERENCES tests(test_id) ON DELETE CASCADE);''')

	conn.execute('''CREATE TABLE IF NOT EXISTS documentLocations(
		document_id INTEGER PRIMARY KEY AUTOINCREMENT,
		document BLOP,
		document_name VARCHAR(100),
		type VARCHAR(20),
		notes_id INTEGER,
		assignment_id INTEGER,
		test_id INTEGER,
		assignmentSolution_id INTEGER,
		testSolution_id INTEGER,
		FOREIGN KEY(notes_id) REFERENCES notes(notes_id) ON DELETE CASCADE,
		FOREIGN KEY(assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
		FOREIGN KEY(test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
		FOREIGN KEY(testSolution_id) REFERENCES testSolutions(solution_id) ON DELETE CASCADE,
		FOREIGN KEY(assignmentSolution_id) REFERENCES assignmentSolutions(solution_id) ON DELETE CASCADE);''')
	
	conn.commit()

def addStudent(conn,name,mail,number,password):
	conn.execute('''INSERT INTO students(student_name,email,contact_number,password)
	VALUES(?,?,?,?);''',(name,mail,number,password))
	conn.commit()

def addTeacher(conn,name,mail,number,password):
	conn.execute('''INSERT INTO teachers(teacher_name,email,contact_number,password)
	VALUES(?,?,?,?);''',(name,mail,number,password))
	conn.commit()

def addSubject(conn,name,teacher_id):
	code=ut.generateCode()
	cmd=conn.execute('''INSERT INTO subjects(subject_name,subject_code)
	VALUES(?,?);''',(name,code))
	subject_id=cmd.lastrowid
	conn.execute('''INSERT INTO handle(teacher_id,subject_id)
	VALUES(?,?);''',(teacher_id,subject_id))
	conn.commit()
	return code,subject_id

def alreadyEnrolled(conn,student_id,subject_id):
	cursor=conn.execute('''SELECT enroll_id FROM enroll WHERE
	student_id == ? AND subject_id == ?;''',(student_id,subject_id))
	res = cursor.fetchone()

	if res:
		return True

	return False

def enrollStudent(conn,student_id,subject_id):
	if not alreadyEnrolled(conn,student_id,subject_id):
		conn.execute('''INSERT INTO enroll(student_id,subject_id)
		VALUES(?,?);''',(student_id,subject_id))
		conn.commit()
		return True

	return False

def newAssignment(conn,content,deadline,subject_id):
	time=ut.getCurrentTime()

	cmd=conn.execute('''INSERT INTO assignments(assignment_content,assignment_deadline
		,subject_id,assignment_assigned_date) VALUES
		(?,?,?,?);''',(content,deadline,subject_id,time))
	assignment_id=cmd.lastrowid
	
	cursor=conn.execute('''SELECT student_id FROM enroll WHERE
		subject_id==?;''',(subject_id,))
	
	for row in cursor.fetchall():
		conn.execute('''INSERT INTO assignmentSolutions(assignment_id,student_id)
		VALUES(?,?);''',(assignment_id,int(row[0])))
	
	conn.commit()
	return assignment_id

def newTest(conn,content,deadline,marks,subject_id):
	time=ut.getCurrentTime()

	cmd=conn.execute('''INSERT INTO tests(test_content,test_deadline
		,subject_id,test_marks,test_assigned_date) VALUES
		(?,?,?,?,?);''',(content,deadline,subject_id,marks,time))
	test_id=cmd.lastrowid
	
	cursor=conn.execute('''SELECT student_id FROM enroll  WHERE
		subject_id==?;''',(subject_id,))
	
	for row in cursor.fetchall():
		conn.execute('''INSERT INTO testSolutions(test_id,student_id)
		VALUES(?,?);''',(test_id,row[0]))
	
	conn.commit()	
	return test_id

def checkTestSolvedFromSolutionId(conn,testSolution_id):
	cursor=conn.execute('''SELECT solution_id FROM testSolutions WHERE
		solution_id==?;''',(testSolution_id,))
	return cursor.fetchone() is not None

def checkAssignmentSolvedFromSolutionId(conn,assignmentSolution_id):
	cursor=conn.execute('''SELECT solution_id FROM assignmentSolutions WHERE
	solution_id==?;''',(assignmentSolution_id,))
	return cursor.fetchone() is not None

def removeUploadedDocuments(conn,docType,Id):
	col=docType+"_id"
	command='''DELETE FROM documentLocations WHERE '''+col+''' == ?;'''
	conn.execute(command,(Id,))
	conn.commit()

def uploadDocument(conn,docType,Id,document,document_name):
	col=docType+"_id"
	if docType == "assignmentSolution":
		if checkAssignmentSolvedFromSolutionId(conn,Id):
			removeUploadedDocuments(conn,docType,Id)
	
	elif docType == "testSolution":
		if checkTestSolvedFromSolutionId(conn,Id):
			removeUploadedDocuments(conn,docType,Id)

	value=(document,document_name,docType,Id)
	command='''INSERT INTO documentLocations(document,document_name,type,'''+col+''')
	VALUES(?,?,?,?)'''
	conn.execute(command,value)

	if docType == "assignmentSolution":
		time=ut.getCurrentTime()
		conn.execute('''UPDATE assignmentSolutions SET submitted_time==?
			WHERE solution_id==?;''',(time,Id))

	elif docType == "testSolution":
		time=ut.getCurrentTime()
		conn.execute('''UPDATE testSolutions SET submitted_time==?
		WHERE solution_id==?;''',(time,Id))

	conn.commit()

def newNotes(conn,subject_id,content):
	time=ut.getCurrentTime()
	cmd=conn.execute('''INSERT INTO notes(subject_id,notes_content,notes_sent)
	VALUES(?,?,?);''',(subject_id,content,time))
	conn.commit()
	return cmd.lastrowid

def getStudentId(conn,mail):
	cursor=conn.execute('''SELECT student_id FROM students WHERE email==?;''',(mail,))
	row=cursor.fetchone()

	if not row:
		return None
	return row[0]

def checkStudentOrTeacher(conn,mail):
	cursor=conn.execute('''SELECT  student_id FROM students WHERE
		email==?;''',(mail,))

	res = cursor.fetchone()
	if res:
		return 'student',res[0]

	cursor=conn.execute('''SELECT teacher_id FROM teachers WHERE
	 	email==?;''',(mail,))

	res = cursor.fetchone()
	if res:
		return 'teacher',res[0]

	return None,None

def getStudentName(conn,student_id):
	cursor=conn.execute('''SELECT student_name FROM students WHERE
	student_id==?;''',(student_id,))
	student_name= cursor.fetchone()
	if student_name:
		student_name=student_name[0]
	return student_name

def getTeacherName(conn,teacher_id):
	cursor=conn.execute('''SELECT teacher_name FROM teachers WHERE
	teacher_id==?;''',(teacher_id,))
	teacher_name =  cursor.fetchone()
	if teacher_name:
		teacher_name = teacher_name[0]
	return teacher_name

def getSubjectName(conn,subject_id):
	cursor=conn.execute('''SELECT subject_name FROM subjects WHERE
	subject_id==?;''',(subject_id,))
	subject_name =  cursor.fetchone()
	if subject_name:
		subject_name = subject_name[0]
	return subject_name

def getPassword(conn,mail):
	user_type,user_id=checkStudentOrTeacher(conn,mail)

	if user_type=='student':
		cursor=conn.execute('''SELECT password FROM students WHERE
		student_id==?;''',(user_id,))
		if cursor is not None:
			return cursor.fetchone()[0]

	elif user_type=='teacher':
		cursor=conn.execute('''SELECT password FROM teachers WHERE
		teacher_id==?;''',(user_id,))
		if cursor is not None:
			return cursor.fetchone()[0]

	return None

def login(conn,mail):
	user_type,user_id=checkStudentOrTeacher(conn,mail)

	if user_type=='student':
		name=getStudentName(conn,user_id)
		time=ut.getCurrentTime()
		conn.execute('''UPDATE students SET login_time=?,logout_time=NULL
		WHERE student_id==?;''',(time,user_id))
		return user_type,name,user_id

	elif user_type=='teacher':
		name=getTeacherName(conn,user_id)
		time=ut.getCurrentTime()
		conn.execute('''UPDATE teachers SET login_time=?,logout_time=NULL
		WHERE teacher_id==?;''',(time,user_id))
		return user_type,name,user_id

	conn.commit()
	return user_type,name,user_id

def isNewUser(conn,email):
	return checkStudentOrTeacher(conn,email)

def signupAsStudent(conn,name,mail,number,password):
	conn.execute('''INSERT INTO students(student_name,email,contact_number,password)
	VALUES(?,?,?,?);''',(name,mail,number,password))
	user_type,name,user_id=login(conn,mail)
	conn.commit()
	return user_type,name,user_id

def signupAsTeacher(conn,name,mail,number,password):
	conn.execute('''INSERT INTO teachers(teacher_name,email,contact_number,password)
	VALUES(?,?,?,?);''',(name,mail,number,password))
	user_type,name,user_id=login(conn,mail)
	conn.commit()
	return user_type,name,user_id

def logout(conn,user_id,user_type):
	time=ut.getCurrentTime()
	
	if user_type == 'teacher':
		conn.execute('''UPDATE teachers SET logout_time=?
		WHERE teacher_id==?;''',(time,user_id))

	else:
		conn.execute('''UPDATE students SET logout_time=?
		WHERE student_id==?;''',(time,user_id))

	conn.commit()

def updatePassword(conn,mail,password,user_type):
	user_type,user_id=checkStudentOrTeacher(conn,mail)

	if user_type == 'student':
		conn.execute('''UPDATE students SET password=? 
			WHERE student_id==?;''',(password,user_id))
		
	elif user_type == 'teacher':
		conn.execute('''UPDATE teachers SET password=? 
			WHERE teacher_id==?;''',(password,user_id))
	conn.commit()

def getSubjectsEnrolled(conn,student_id):
	cursor=conn.execute('''SELECT  subjects.subject_id,subject_name,teacher_name FROM subjects,handle,teachers,enroll
		WHERE subjects.subject_id==handle.subject_id AND
		handle.teacher_id==teachers.teacher_id AND
		subjects.subject_id==enroll.subject_id AND
		enroll.student_id == ?;''',(student_id,))
	return cursor.fetchall()

def getDataOfMainPageForStudents(conn,student_id):
	subs=[]
	data=getSubjectsEnrolled(conn,student_id)

	for row in data:
		cursor2=conn.execute('''SELECT  COUNT(*) FROM assignments,assignmentSolutions
			WHERE assignments.assignment_id==assignmentSolutions.assignment_id AND
			assignments.subject_id==? AND assignmentSolutions.student_id == ?;''',(int(row[0]),student_id))
		acount=cursor2.fetchone()
		if acount:
			acount=acount[0]
		else:
			acount=0

		cursor2=conn.execute('''SELECT  COUNT(*) FROM tests,testSolutions
			WHERE tests.test_id==testSolutions.test_id AND
			tests.subject_id==? AND testSolutions.student_id == ?;''',(int(row[0]),student_id))
		tcount=cursor2.fetchone()
		if tcount:
			tcount=tcount[0]
		else:
			tcount=0

		subs.append((row[0],row[1],row[2],acount,tcount))
	return subs

def getNumberOfStudentsEnrolled(conn,subject_id):
	cursor=conn.execute('''SELECT COUNT(*) FROM enroll 
		WHERE subject_id==?;''',(subject_id,))
	count = cursor.fetchone()[0]	
	if count is None:
		count=0
	return count

def getSubjectsHandled(conn,teacher_id):
	cursor=conn.execute('''SELECT subjects.subject_id,subject_name,subject_code FROM subjects,handle
	WHERE handle.teacher_id == ? AND handle.subject_id==subjects.subject_id;''',(teacher_id,))
	return cursor.fetchall()

def getDataOfMainPageForTeachers(conn,teacher_id):
	subs=[]
	data=getSubjectsHandled(conn,teacher_id)
	
	for row in data:
		student_count=getNumberOfStudentsEnrolled(conn,row[0])

		cursor=conn.execute('''SELECT COUNT(*) FROM assignmentSolutions,assignments WHERE
			assignments.assignment_id==assignmentSolutions.assignment_id AND
			subject_id ==? AND submitted_time IS NULL 
			GROUP BY assignments.assignment_id HAVING COUNT(*)<=?;''',(row[0],student_count))
		assignment_count=cursor.fetchone()
		
		if assignment_count is None:
			assignment_count=0

		cursor=conn.execute('''SELECT COUNT(*) FROM testSolutions,tests WHERE
			tests.test_id==testSolutions.test_id AND
			subject_id ==? AND submitted_time IS NULL
			GROUP BY tests.test_id HAVING COUNT(*)<=?;''',(row[0],student_count))
		test_count=cursor.fetchone()
		
		if test_count is None:
			test_count=0

		subs.append((row[0],row[1],row[2],assignment_count,test_count,student_count))

	return subs

def getSubjectId(conn,code):
	cursor=conn.execute('''SELECT subject_id,subject_name FROM subjects WHERE
	subject_code == ?;''',(code,))
	row=cursor.fetchone()
	if row:
		return row[0],row[1]
	else:
		return None,None

def unEnroll(conn,student_id,subject_id):
	conn.execute('''DELETE FROM enroll WHERE
	student_id == ? AND subject_id == ?;''',(student_id,subject_id))
	conn.commit()

def removeSubject(conn,subject_id):
	conn.execute('''DELETE FROM handle WHERE
	subject_id == ?;''',(subject_id,))

	conn.execute('''DELETE FROM subjects WHERE
	subject_id == ?;''',(subject_id,))

	conn.execute('''DELETE FROM enroll WHERE
	subject_id == ?;''',(subject_id,))

	conn.commit()

def handledBy(conn,subject_id):
	cursor=conn.execute('''SELECT teacher_name FROM teachers,handle WHERE
	teachers.teacher_id == handle.teacher_id AND
	subject_id == ?;''',(subject_id,))
	teacher_name=cursor.fetchone()
	if teacher_name:
		teacher_name=teacher_name[0]
	return teacher_name

def getBriefNotesDetails(conn,subject_id):
	cursor=conn.execute('''SELECT notes_id,notes_sent FROM notes WHERE
	subject_id == ? ORDER BY notes_sent;''',(subject_id,))
	return cursor.fetchall() 

def getNotes(conn,notes_id):
	cursor = conn.execute('''SELECT notes_content,notes_sent FROM notes WHERE
		notes_id == ?;''',(notes_id,))
	notes=cursor.fetchone()
	
	if notes is not None:
		notes=list(notes)
		cursor = conn.execute('''SELECT document_id,document_name FROM documentLocations WHERE
		notes_id == ?;''',(notes_id,))
		docs=cursor.fetchall()
		notes.append(list(docs))
	
	return notes

def downloadDocument(conn,document_id):
	cursor=conn.execute('''SELECT document,document_name from documentLocations WHERE
	document_id == ?;''',(document_id,))
	return cursor.fetchone()

def getAssignmentsNotCompleted(conn,subject_id,student_id):
	cursor=conn.execute('''SELECT assignments.assignment_id,
		assignment_assigned_date FROM assignments,assignmentSolutions WHERE
		assignments.assignment_id==assignmentSolutions.assignment_id AND
		subject_id==? AND student_id==?
		AND submitted_time IS ?;''',(subject_id,student_id,None))
	
	return cursor.fetchall()

def getAssignmentsCompleted(conn,subject_id,student_id):
	time=ut.getCurrentTime()
	
	cursor=conn.execute('''SELECT assignments.assignment_id,assignment_assigned_date
		FROM assignments,assignmentSolutions WHERE
		assignments.assignment_id==assignmentSolutions.assignment_id AND
		subject_id==? AND student_id==? AND
		submitted_time<=?;''',(subject_id,student_id,time))
	
	return cursor.fetchall()

def getAssignmentsForStudents(conn,subject_id,student_id):
	completed=getAssignmentsCompleted(conn,subject_id,student_id)
	not_completed=getAssignmentsNotCompleted(conn,subject_id,student_id)

	return completed+not_completed

def getAssignmentsForTeachers(conn,subject_id):
	cursor=conn.execute('''SELECT assignment_id,
		assignment_assigned_date FROM assignments WHERE
		subject_id==? ORDER BY assignment_deadline;''',(subject_id,))

	return cursor.fetchall()

def getAssignmentDetails(conn,assignment_id):
	cursor=conn.execute('''SELECT assignment_content,assignment_assigned_date,
		assignment_deadline FROM assignments WHERE
		assignment_id==?;''',(assignment_id,))
	assignments=cursor.fetchone()
	
	if assignments is not None:
		assignments=list(assignments)
		cursor = conn.execute('''SELECT document_id,document_name FROM documentLocations WHERE
		assignment_id == ?;''',(assignment_id,))
		docs=cursor.fetchall()
		assignments.append(list(docs))
	
	return assignments

def getTestsNotCompleted(conn,subject_id,student_id):
	cursor=conn.execute('''SELECT tests.test_id,test_assigned_date
		FROM tests,testSolutions WHERE tests.test_id==testSolutions.test_id 
		AND subject_id==? AND student_id==? 
		AND submitted_time IS ?;''',(subject_id,student_id,None))

	return cursor.fetchall()

def getTestsCompleted(conn,subject_id,student_id):
	time=ut.getCurrentTime()
	
	cursor=conn.execute('''SELECT tests.test_id,test_assigned_date
		FROM tests,testSolutions WHERE
		tests.test_id==testSolutions.test_id AND
		subject_id==? AND student_id==? AND
		submitted_time<=?;''',(subject_id,student_id,time))

	return cursor.fetchall()

def getTestsForStudents(conn,subject_id,student_id):
	completed=getTestsCompleted(conn,subject_id,student_id)
	not_completed=getTestsNotCompleted(conn,subject_id,student_id)

	return completed+not_completed

def getTestsForTeachers(conn,subject_id):
	cursor=conn.execute('''SELECT test_id,test_deadline,
		test_assigned_date FROM tests WHERE
		subject_id==? ORDER BY test_deadline;''',(subject_id,))

	return cursor.fetchall()

def getTestDetails(conn,test_id):
	cursor=conn.execute('''SELECT test_content,test_assigned_date,test_deadline FROM tests WHERE
	test_id==?;''',(test_id,))
	tests=cursor.fetchone()
	
	if tests is not None:
		tests=list(tests)
		cursor = conn.execute('''SELECT document_id,document_name FROM documentLocations WHERE
		test_id == ?;''',(test_id,))
		docs=cursor.fetchall()
		tests.append(list(docs))

	cursor=conn.execute('''SELECT test_marks FROM tests WHERE
	test_id==?;''',(test_id,))
	marks=cursor.fetchone()[0]
	tests.append(marks)
	
	return tests

def getAssignmentSubmittedCount(conn,assignment_id):
	cursor=conn.execute('''SELECT COUNT(*) FROM assignmentSolutions WHERE
	assignment_id==?;''',(assignment_id,))
	return cursor.fetchone()[0]

def getAssignmentSolutionsOfStudents(conn,assignment_id):
	cursor=conn.execute('''SELECT students.student_id,student_name,submitted_time
	FROM assignmentSolutions,students WHERE
	assignmentSolutions.student_id==students.student_id AND
	assignment_id==? AND submitted_time IS NOT ?;''',(assignment_id,None))
	return cursor.fetchall()

def getAssignmentSolution(conn,student_id,assignment_id):
	cursor=conn.execute('''SELECT solution_id,submitted_time FROM assignmentSolutions WHERE
	student_id==? AND assignment_id==?;''',(student_id,assignment_id))

	solution=cursor.fetchone()

	if solution:
		solution=list(solution)
		cursor=conn.execute('''SELECT document_id,document_name FROM documentLocations WHERE
			assignmentSolution_id==?;''',(solution[0],))
		solution.append(cursor.fetchall())

	return solution

def getTestSolutionsOfStudents(conn,test_id):
	cursor=conn.execute('''SELECT students.student_id,student_name,submitted_time
	FROM testSolutions,students WHERE
	testSolutions.student_id==students.student_id AND
	test_id==?''',(test_id,))
	return cursor.fetchall()

def getTestSubmittedCount(conn,test_id):
	cursor=conn.execute('''SELECT COUNT(*) FROM testSolutions WHERE
	test_id==?;''',(test_id,))
	return cursor.fetchone()[0]

def getTestSolution(conn,student_id,test_id):
	cursor=conn.execute('''SELECT solution_id,submitted_time FROM testSolutions WHERE
		test_id==? AND student_id==?;''',(test_id,student_id))

	solution=cursor.fetchone()

	if solution:
		solution=list(solution)
		cursor=conn.execute('''SELECT document_id,document_name FROM documentLocations WHERE
		testSolution_id==?;''',(solution[0][0],))
		solution.append(cursor.fetchall())

	return solution

def giveScoreToTests(conn,test_id,student_id,score):
	conn.execute('''UPDATE testSolutions SET test_score=? WHERE
	test_id==? AND student_id==?;''',(score,test_id,student_id))
	conn.commit()

def checkAssignmentSolved(conn,assignment_id,student_id):
	solution_id = getAssignmentSolutionId(conn,assignment_id,student_id)
	return solution_id is not None

def getAssignmentSolutionId(conn,assignment_id,student_id):
	cursor=conn.execute('''SELECT solution_id FROM assignmentSolutions WHERE
	student_id==? AND assignment_id==?;''',(student_id,assignment_id))
	return cursor.fetchone()

def getAssignmentSolutionDocument(conn,assignmentSolution_id):
	cursor=conn.execute('''SELECT document_id,document_name FROM documentLocations 
		WHERE assignmentSolution_id==?;''',(assignmentSolution_id,))
	return cursor.fetchall()

def checkTestSolved(conn,student_id,test_id):
	solution_id =  getTestSolution_id(conn,test_id,student_id)
	return solution_id is not None

def getTestSolution_id(conn,test_id,student_id):
	cursor=conn.execute('''SELECT solution_id FROM testSolutions WHERE
		test_id==? AND student_id==?;''',(test_id,student_id))
	return cursor.fetchone()

def getTestSolutionDocument(conn,testSolution_id):
	cursor=conn.execute('''SELECT document_id,document_name FROM documentLocations WHERE
		testSolution_id==?;''',(testSolution_id,))
	return cursor.fetchall()

def getTestScore(conn,testSolution_id):
	cursor=conn.execute('''SELECT test_score FROM testSolutions WHERE
	solution_id==?;''',(testSolution_id,))
	return cursor.fetchone()[0]

def getTestDeadlineAndMarks(conn,test_id):
	cursor=conn.execute('''SELECT test_deadline,test_marks FROM tests WHERE
	test_id==?;''',(test_id,))
	return cursor.fetchone()

def getAssignmentDeadline(conn,assignment_id):
	cursor=conn.execute('''SELECT assignment_deadline FROM assignments WHERE
	assignment_id==?;''',(assignment_id,))
	return cursor.fetchone()[0]

def getMailAddressOfStudent(conn,student_id):
	cursor=conn.execute('''SELECT email FROM students WHERE
	student_id==?;''',(student_id,))
	return cursor.fetchone()[0]

def getMailAddressOfTeacher(conn,teacher_id):
	cursor=conn.execute('''SELECT email FROM teachers WHERE
		teacher_id==?;''',(teacher_id,))
	return cursor.fetchone()[0]

def getMailAddressOfEnrolledStudents(conn,subject_id):
	cursor=conn.execute('''SELECT email FROM students,enroll WHERE
	enroll.student_id==students.student_id AND
	subject_id==?;''',(subject_id,))
	return cursor.fetchall()

def getLoginTime(conn,user_id,user_type):
	if user_type == 'student':
		cursor=conn.execute('''SELECT login_time FROM students WHERE
		student_id==?;''',(user_id,))

	else:
		cursor=conn.execute('''SELECT login_time FROM teachers WHERE
		teacher_id==?;''',(user_id,))
	
	time= cursor.fetchone()

	if time:
		time =  time[0]

	return time

def getLogoutTime(conn,user_id,user_type):
	if user_type == 'student':
		cursor=conn.execute('''SELECT logout_time FROM students WHERE
		student_id==?;''',(user_id,))

	else:
		cursor=conn.execute('''SELECT logout_time FROM teachers WHERE
		teacher_id==?;''',(user_id,))
	
	return cursor.fetchone()