import database as db

class MainPage:
	def __init__(self,login):
		self.user=login

	def getDataOfMainPage(self):
		if self.user.user_type=='teacher':
			return db.getDataOfMainPageForTeachers(self.user.conn,self.user.user_id)

		elif self.user.user_type=='student':
			return db.getDataOfMainPageForStudents(self.user.conn,self.user.user_id)

		else:
			return None