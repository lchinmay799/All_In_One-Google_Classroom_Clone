import database as db
import utilities as ut

class Assignments:
	def __init__(self,login,subject):
		self.user=login
		self.subject=subject

	def getAssignments(self):
		if self.user.user_type=='student':
			return db.getAssignmentsForStudents(self.user.conn,self.subject.subject_id,self.user.user_id)

		else:
			return db.getAssignmentsForTeachers(self.user.conn,self.subject.subject_id)

	def uploadAssignment(self,content,deadline):
		return db.newAssignment(self.user.conn,content,deadline,self.subject.subject_id)

	def getAssignmentDetails(self,assignment_id):
		return db.getAssignmentDetails(self.user.conn,assignment_id)

	def uploadDocument(self,file,assignment_id,filename):
		db.uploadDocument(self.user.conn,'assignment',assignment_id,file,filename)

	def showUploadMessage(self):
		message='''New Assignment Posted Successfully\n\n'''+str(ut.getCurrentTime())
		ut.showMessageBox("Posted Successfully",message,"information")

	def downloadDocument(self,document_id):
		return db.downloadDocument(self.user.conn,document_id)

	def isAssignmentSolved(self,assignment_id):
		return db.checkAssignmentSolved(self.user.conn,assignment_id,self.user.user_id)

	def getAssignmentSolutionUploaded(self,assignment_id):
		solution_id=db.getAssignmentSolutionId(self.user.conn,assignment_id,self.user.user_id)
		return db.getAssignmentSolutionDocument(self.user.conn,solution_id[0])

	def getAssignmentDeadline(self,assignment_id):
		return db.getAssignmentDeadline(self.user.conn,assignment_id)