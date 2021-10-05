import database as db
import utilities as ut

class Tests:
	def __init__(self,login,subject):
		self.user=login
		self.subject=subject

	def getTests(self):
		if self.user.user_type=='student':
			return db.getTestsForStudents(self.user.conn,self.subject.subject_id,self.user.user_id)

		else:
			return db.getTestsForTeachers(self.user.conn,self.subject.subject_id)

	def getTestDetails(self,test_id):
		return db.getTestDetails(self.user.conn,test_id)

	def uploadTest(self,content,deadline,marks):
		return db.newTest(self.user.conn,content,deadline,marks,self.subject.subject_id)

	def uploadDocument(self,file,test_id,filename):
		db.uploadDocument(self.user.conn,'test',test_id,file,filename)

	def showUploadMessage(self):
		message='''New Test Posted Successfully\n\n'''+str(ut.getCurrentTime())
		ut.showMessageBox("Posted Successfully",message,"information")

	def downloadDocument(self,document_id):
		return db.downloadDocument(self.user.conn,document_id)

	def isTestSolved(self,test_id):
		return db.checkTestSolved(self.user.conn,self.user.user_id,test_id)

	def getTestScore(self,test_id,student_id):
		solution_id=db.getTestSolution_id(self.user.conn,test_id,student_id)
		return db.getTestScore(self.user.conn,solution_id[0])

	def getTestSolutionUploaded(self,test_id):
		solution_id=db.getTestSolution_id(self.user.conn,test_id,self.user.user_id)
		return db.getTestSolutionDocument(self.user.conn,solution_id[0])

	def getTestDeadlineAndMarks(self,test_id):
		return db.getTestDeadlineAndMarks(self.user.conn,test_id)