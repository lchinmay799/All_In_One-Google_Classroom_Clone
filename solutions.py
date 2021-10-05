import database as db
import utilities as ut

class Solutions:
	def __init__(self,login):
		self.user=login
		self.test_id=None
		self.assignment_id=None

	def setTestId(self,test_id):
		self.test_id=test_id

	def setAssignmentId(self,assignment_id):
		self.assignment_id=assignment_id

	def getAllAssignmentSolutions(self):
		return db.getAssignmentSolutionsOfStudents(self.user.conn,self.assignment_id)

	def getAssignmentSubmittedCount(self):
		return db.getAssignmentSubmittedCount(self.user.conn,self.assignment_id)

	def getTestSubmittedCount(self):
		return db.getTestSubmittedCount(self.user.conn,self.test_id)

	def getAllTestSolutions(self):
		return db.getTestSolutionsOfStudents(self.user.conn,self.test_id)

	def getTestSolution(self,student_id):
		return db.getTestSolution(self.user.conn,student_id,self.test_id)

	def getAssignmentSolution(self,student_id):
		return db.getAssignmentSolution(self.user.conn,student_id,self.assignment_id)

	def downloadDocument(self,document_id):
		return db.downloadDocument(self.user.conn,document_id)

	def giveScore(self,score,student_id):
		db.giveScoreToTests(self.user.conn,self.test_id,student_id,score)

	def showScoreMessage(self,student_id,score):
		name=db.getStudentName(self.user.conn,student_id)
		message='''YOU GAVE '''+str(score)+''' MARKS TO '''+name
		ut.showMessageBox("Evaluation Done",message,"information")

	def uploadSolution(self,document,document_name,Id,docType):
		db.uploadDocument(self.user.conn,docType,Id,document,document_name)