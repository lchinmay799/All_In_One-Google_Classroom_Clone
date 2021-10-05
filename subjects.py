import database as db
import utilities as ut

class Subjects:
	def __init__(self,login):
		self.subjects=None
		self.user=login
		self.subject_id=None

	def setSubjects(self,subjects):
		self.subjects=subjects

	def noSubjects(self):
		return self.subjects is None or len(self.subjects)==0

	def newSubject(self,subject_name):
		return db.addSubject(self.user.conn,subject_name,self.user.user_id)

	def setCurrentSubject(self,subject_id):
		self.subject_id=subject_id

	def checkValidCode(self,code):
		return db.getSubjectId(self.user.conn,code)

	def enrollToNewSubject(self,subject_id):
		self.setCurrentSubject(subject_id)
		subject_name = self.getSubjectName()

		if db.enrollStudent(self.user.conn,self.user.user_id,subject_id):
			message = '''Welcome  '''+self.user.user_name+''' to '''+subject_name
			ut.showMessageBox("Welcome",message,"information")
		
		else:
			message = '''Hey '''+self.user.user_name+''', You are already Enrolled in '''+subject_name
			ut.showMessageBox("Already Enrolled",message,"warning")

	def unenrollFromSubject(self):
		db.unEnroll(self.user.conn,self.user.user_id,self.subject_id)

	def removeSubject(self):
		db.removeSubject(self.user.conn,self.subject_id) 

	def getSubjectName(self):
		return db.getSubjectName(self.user.conn,self.subject_id)

	def getTeacherName(self):
		return db.handledBy(self.user.conn,self.subject_id)

	def getTeacherHandlingTheSubject(self):
		return db.handledBy(self.user.conn,self.subject_id)

	def getEnrolledStudentsMailAddress(self):
		return db.getMailAddressOfEnrolledStudents(self.user.conn,self.subject_id)		