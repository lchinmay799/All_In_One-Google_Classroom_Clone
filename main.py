from flask import Flask,render_template,redirect,request,url_for,send_file
from datetime import datetime
import random
from io import BytesIO

import database as db
import utilities as ut
import login as log
import signup as sign
import mainPage as mp
import resetPassword as reset
import connection as connection
import subjects as sub
import notes as nt
import tests as tst
import assignments as asmt
import solutions as sol

app=Flask(__name__)
connect,login,subject,note,test,assignment,solution=None,None,None,None,None,None,None

@app.route('/')
def homePage():
	return render_template('homePage.html',loggedIn = False)

@app.route('/homePage',methods=['GET','POST'])
def homePage2():
	loggedIn=True
	time=ut.getCurrentTime()
	loginTime=login.getLoginTime()

	if not loginTime:
		return render_template('homePage.html',loggedIn = False)

	diff_hr,diff_min=ut.getDifference(time,loginTime)

	if (diff_hr>24 or (diff_hr ==24 and diff_min>=0)):
		login.logout()
		loggedIn = False

	else:
		logout_Time=login.getLogoutTime()
		if logout_Time[0]:
			loggedIn = False

	return render_template('homePage.html',loggedIn = loggedIn)

@app.route('/login',methods=['GET','POST'])
def login():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	fromPage=request.form.get('pageName')

	if fromPage == 'reset':
		rp=reset.ResetPassword(login)
		email=request.form.get('email')
		password1=request.form.get('password')
		password2=request.form.get('confirmPassword')

		if ut.checkEquality(password1,password2):
			user_type=rp.checkNewUser(email)

			if user_type is None:
				rp.noAccount()
				return render_template('signup.html')

			else:
				rp.resetPassword(email,password1,user_type)
				rp.passwordUpdated()
				return render_template('login.html')

		else:
			rp.passwordsDoNotMatch()
			return render_template('resetPassword.html')

	else:
		return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	return render_template('signup.html')

@app.route('/reset',methods=['GET','POST'])
def resetPassword():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	return render_template('resetPassword.html')

@app.route('/mainPage',methods=['GET','POST'])
def mainPage():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	if request.form.get("logout"):
		login.logout()
		return redirect('homePage')

	success=False
	fromPage=request.form.get("pageName")

	if fromPage == 'login':
		email=request.form.get('email')
		input_password=request.form.get('password')
		
		if login.checkNewUser(email):
			login.noAccount()
			return render_template('signup.html')

		else:
			actual_password=db.getPassword(connect.conn,email)

			if login.checkPassword(actual_password,input_password):
				login.login(email)
				success=True

			else:
				login.wrongPassword()
				return render_template('login.html')

	elif fromPage == 'signup':
		signup=sign.Signup(login)
		email=request.form.get('email')
		user_type,user_id=db.checkStudentOrTeacher(connect.conn,email)

		if user_type is None and user_id is None:
			user_name=request.form.get('username')
			contact=request.form.get('contact')
			password1=request.form.get('password')
			password2=request.form.get('confirmPassword')

			if ut.checkEquality(password1,password2):
				success=True
				user_type=request.form.get('userType')

				if user_type == 'Teacher':
					signup.signupAsTeacher(user_name,email,contact,password1)

				else:
					signup.signupAsStudent(user_name,email,contact,password1)
			
			else:
				signup.passwordsDoNotMatch()
				return render_template('signup.html')
		
		else:
			signup.hasAccount()
			return render_template('login.html')

	elif fromPage == 'subjects' or fromPage == 'newSubject' or fromPage == 'homepage':
		success=True

	if success:
		mainpage=mp.MainPage(login)
		subject.setSubjects(mainpage.getDataOfMainPage())
		colors=None
		
		if subject.noSubjects():

			if login.isTeacher():
				message="YOU ARE NOT HANDLING ANY SUBJECTS"
				button="CREATE CLASSROOM"
				target='newSubject'

			else:
				message="YOU ARE NOT ENROLLED IN ANY SUBJECTS"
				button="ENROLL"
				target='enroll'

		else:

			if login.isTeacher():
				message=None
				button="CREATE CLASSROOM"
				target='newSubject'

			else:
				message=None
				button="ENROLL"
				target='enroll'
			
			colors=ut.getColors(len(subject.subjects))
		
		return render_template('mainPage.html',subject=subject,message=message,button=button,target=target,colors=colors)

@app.route('/enroll',methods=['GET','POST'])
def enroll():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	code=ut.dialogForCode()
	subject_id,subject_name=subject.checkValidCode(code)
	
	if not subject_name:
		message = '''You have entered an Invalid Subject Code \n\n Kindly Enroll with the Correct Code'''
		ut.showMessageBox("Invalid Code",message,"error")
		mainpage=mp.MainPage(login)
		subject.setSubjects(mainpage.getDataOfMainPage())
		colors=None
		
		if subject.noSubjects():

			if login.isTeacher():
				message="YOU ARE NOT HANDLING ANY SUBJECTS"
				button="CREATE CLASSROOM"
				target='newSubject'

			else:
				message="YOU ARE NOT ENROLLED IN ANY SUBJECTS"
				button="ENROLL"
				target='enroll'

		else:
			if login.isTeacher():
				message=None
				button="CREATE CLASSROOM"
				target='newSubject'

			else:
				message=None
				button="ENROLL"
				target='enroll'
			colors=ut.getColors(len(subject.subjects))
		return render_template('mainPage.html',subject=subject,message=message,button=button,target=target,colors=colors)

	else:
		subject.enrollToNewSubject(subject_id)

		subject_name = subject.getSubjectName()
		teacher_name=subject.getTeacherHandlingTheSubject()
		ToAddress=login.getMailAddress()
		ut.sendSuccessfulEnrollmentMail(ToAddress,subject_name,login.user_name,teacher_name)

		return redirect('/subjects')

@app.route('/unenroll',methods=['GET','POST'])
def unenroll():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	res=False

	if login.isTeacher():
		message='''Do you want to Remove the Subject ? '''
		res=ut.askQuestion("Remove",message)
		
		if res:
			subject.removeSubject()
			message='''Removed the Subject Successfully ...'''
			title="Subject Removed"

	else:
		
		message='''Do you want to Unenroll From the Subject ? '''
		res=ut.askQuestion("Unenroll",message)
	
		if res:
			subject.unenrollFromSubject()
			message = "Unenrolled From the Subject Successfully"
			title = "Unenrolled"

	if res:
		ut.showMessageBox("Subject Removed",message,"information")
		return redirect('/homePage')

	else:

		if login.isTeacher():
			button="REMOVE"

		else:
			button="UNENROLL"

		return redirect('/subjects')

@app.route('/subjects',methods=['GET','POST'])
def subjects():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	fromPage=request.form.get('pageName')
	subject_name=""

	if login.isTeacher():
		button="REMOVE"
		
		if fromPage == 'newSubject':
			subject_name=request.form.get('subjectName')
			code,subject_id=subject.newSubject(subject_name)
			message='''Classroom for '''+subject_name+''' is created Successfully \n\n Code is '''+code
			ut.showMessageBox("Classroom Code",message,"information")
			subject.setCurrentSubject(subject_id)

		elif fromPage == 'mainPage':
			subject_id=request.form.get('subject')
			subject.setCurrentSubject(subject_id)
	
	else:
		button="UNENROLL"
		
		if fromPage == 'mainPage':
			subject_id=request.form.get('subject')
			subject.setCurrentSubject(subject_id)

	subject_name=subject.getSubjectName()
	return render_template('subjects.html',button=button,subject_name=subject_name.upper())

@app.route('/newSubject',methods=['GET','POST'])
def newSubject():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	return render_template('newSubject.html')

@app.route('/notes',methods=['POST','GET'])
def notes():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	notes=note.getBriefNotesDetails()
	teacher_name=subject.getTeacherName()
	teacher = False
	message=None

	if login.isTeacher():
		teacher=True
		
		if not notes:
			message="YOU HAVE NOT UPLOADED ANY NOTES"
			
	else:

		if not notes:
			message="NO NOTES ARE UPLOADED"

	return render_template('notes.html',notes=notes,message=message,
		teacher_name=teacher_name,teacher=teacher)

@app.route('/assignments',methods=['POST','GET'])
def assignments():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	assignments=assignment.getAssignments()
	teacher_name=subject.getTeacherName()
	teacher=False
	message=None

	if login.isTeacher():
		teacher = True

		if not assignments:
			message = "YOU HAVE NOT POSTED ANY ASSIGNMENTS"

	else:

		if not assignments:
			message="NO ASSIGNMENTS ARE UPLOADED"

	return render_template('assignments.html',message=message,assignments=assignments,
		teacher_name=teacher_name,teacher=teacher)

@app.route('/tests',methods=['POST','GET'])
def tests():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	tests=test.getTests()
	teacher_name=subject.getTeacherName()
	teacher=False
	message=None

	if login.isTeacher():
		teacher = True

		if not tests:
			message = "YOU HAVE NOT POSTED ANY TESTS"

	else:

		if not tests:
			message="NO TESTS ARE ASSIGNED"

	return render_template('tests.html',message=message,tests=tests,
		teacher_name=teacher_name,teacher=teacher)

@app.route('/upload',methods=['GET','POST'])
def upload():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	fromPage=request.args.get('type')
	datetime=ut.getCurrentTime()
	date=datetime.date().strftime("%d-%m-%Y")
	return render_template('upload.html',pageName=fromPage,date=date)

@app.route('/newDocument',methods=['GET','POST'])
def newDocument():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	fromPage=request.form.get('pageName')
	content=request.form.get('content')
	files = request.files.getlist('files')

	subject_name=subject.getSubjectName()
	teacher_name=subject.getTeacherHandlingTheSubject()
	ToAddress = subject.getEnrolledStudentsMailAddress()


	if fromPage == 'notes':
		note_id=note.uploadNotes(content)
		for file in files:
			if file.filename != '':
				note.uploadDocument(file.read(),note_id,file.filename)
		
		note.showUploadMessage()
		ut.newNotesMail(ToAddress,subject_name,teacher_name)

		return redirect('/notes')

	elif fromPage == 'assignments':
		date=request.form.get('date')
		time=request.form.get('time')
		deadline=ut.createDatetime(date+" "+time)
		
		assignment_id=assignment.uploadAssignment(content,deadline)
		
		for file in files:
			if file.filename!='':
				assignment.uploadDocument(file.read(),assignment_id,file.filename)

		assignment.showUploadMessage()
		ut.newAssignmentMail(ToAddress,subject_name,teacher_name,deadline)

		return redirect('/assignments')
	
	elif fromPage == 'tests':
		date=request.form.get('date')
		time=request.form.get('time')
		marks=request.form.get('marks')
		deadline=ut.createDatetime(date+" "+time)
		
		test_id=test.uploadTest(content,deadline,marks)
		
		for file in files:
			if file.filename!='':
				test.uploadDocument(file.read(),test_id,file.filename)

		test.showUploadMessage()
		ut.newTestMail(ToAddress,subject_name,teacher_name,deadline,marks)

		return redirect('/tests')
	
@app.route('/notesDetails',methods=['GET','POST'])
def notesDetails():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	if login.isTeacher() and request.form.get('upload'):
		fromPage = request.form.get('pageName')
		return redirect(url_for('upload',type=fromPage))
	
	note_id = request.form.get('note')
	notes=note.getNotes(note_id)
	return render_template('notesDetails.html',notes=notes)

@app.route('/ATDetails',methods=['GET','POST'])
def ATDetails():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	fromPage = request.form.get('pageName')
	teacher=login.isTeacher()

	if teacher and request.form.get('upload'):
		return redirect(url_for('upload',type=fromPage))

	Id=None
	solved_data=None
	deadline=None
	score=None
	marks=None
	
	if fromPage == 'tests':
		Id=request.form.get('test')
		solution.setTestId(Id)
		data=test.getTestDetails(Id)
		deadline,marks=test.getTestDeadlineAndMarks(Id)

		if not teacher and test.isTestSolved(Id):
			score=test.getTestScore(Id,login.user_id)
			solved_data=test.getTestSolutionUploaded(Id)
	
	else:
		Id=request.form.get('assignment')
		solution.setAssignmentId(Id)
		data=assignment.getAssignmentDetails(Id)
		deadline=assignment.getAssignmentDeadline(Id)

		if not teacher and assignment.isAssignmentSolved(Id):
			solved_data=assignment.getAssignmentSolutionUploaded(Id)

	time=ut.getCurrentTime()
	deadline=ut.createDatetime2(deadline)
	canBeUpdated=str(time<=deadline)

	return render_template('ATDetails.html',data=data,pageName=fromPage,marks=marks,
		teacher=teacher,Id=Id,solved_data=solved_data,score=score,canBeUpdated=canBeUpdated)

@app.route('/downloadDocuments',methods=['GET','POST'])
def downloadDocuments():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	document_id=int(request.form.get('file'))
	document,document_name=note.downloadDocument(document_id)
	return send_file(BytesIO(document),download_name=document_name,as_attachment=True)

@app.route('/solutions',methods=['GET','POST'])
def solutions():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	solution_type=request.form.get('upload')
	message = None
	
	if solution_type == 'tests' or solution_type == 'assignments':
		Id=request.form.get("Id")
		files = request.files.getlist('files')
		
		if solution_type == 'tests':
			sol_type='testSolution'
			title="Test Answered"
		
		else:
			sol_type='assignmentSolution'
			title="Assignment Solved"

		for file in files:
			if file.filename!='':
				solution.uploadSolution(file.read(),file.filename,Id,sol_type)

		message='''Solution Uploaded Successfully '''
		ut.showMessageBox(title,message,"information")

		return redirect("/"+solution_type)
	
	else:
		solution_type=request.form.get('details')
		if solution_type == 'tests':
			data=solution.getAllTestSolutions()
			count=solution.getTestSubmittedCount()

		else:
			data=solution.getAllAssignmentSolutions()
			count=solution.getAssignmentSubmittedCount()
			

	if not data:
		message="NO STUDENTS HAVE ANSWERED THE "+solution_type[:-1].upper()

	return render_template('solutions.html',data=data,toPage=solution_type,message=message,count=count)

@app.route('/solutionDetails',methods=['POST','getlist'])
def solutionDetails():
	if request.form.get('logo1.x') or request.form.get('logo2.x'):
		return redirect('homePage')

	fromPage=request.form.get('pageName')
	student_id=request.form.get('solution')

	if fromPage == 'assignments':
		data=solution.getAssignmentSolution(student_id)

	elif fromPage == 'tests':
		data=solution.getTestSolution(student_id)

	return render_template('solutionDetails.html',data=data,toPage=fromPage)

if __name__=='__main__':
	connect=connection.Database('AllInOne.db')
	connect.connect()
	
	login=log.Login(connect.conn)
	subject=sub.Subjects(login)
	note=nt.Notes(login,subject)
	test=tst.Tests(login,subject)
	assignment=asmt.Assignments(login,subject)
	test=tst.Tests(login,subject)
	solution=sol.Solutions(login)
	
	# while running for the first time
	connect.createTables()
	
	app.run(debug=True)