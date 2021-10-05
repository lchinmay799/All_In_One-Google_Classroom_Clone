import database as db
import utilities as ut

class Notes:
	def __init__(self,login,subject):
		self.user=login
		self.subject=subject

	def getNotes(self,note_id):
		return db.getNotes(self.user.conn,note_id)

	def getBriefNotesDetails(self):
		return db.getBriefNotesDetails(self.user.conn,self.subject.subject_id)

	def uploadNotes(self,content):
		return db.newNotes(self.user.conn,self.subject.subject_id,content)

	def uploadDocument(self,file,note_id,filename):
		db.uploadDocument(self.user.conn,'notes',note_id,file,filename)

	def showUploadMessage(self):
		message='''New Notes Posted Successfully\n\n'''+str(ut.getCurrentTime())
		ut.showMessageBox("Posted Successfully",message,"information")

	def downloadDocument(self,document_id):
		return db.downloadDocument(self.user.conn,document_id)