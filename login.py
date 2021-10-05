import utilities as ut
import database as db

class Login:
	def __init__(self,conn):
		self.conn=conn
		self.user_id=None
		self.user_type=None
		self.user_name=None

	def checkPassword(self,actual_password,input_password):
		return ut.checkEquality(actual_password,input_password)

	def getOTP(self):
		generatedOTP=random.randint(100000,999999)
		enteredOTP=ut.dialogForOtp()

	def checkNewUser(self,email):
		user_type,user_id=db.isNewUser(self.conn,email)
		return user_id is None

	def login(self,email):
		self.user_type,self.user_name,self.user_id = db.login(self.conn,email)
		message="WELCOME "+self.user_name
		ut.showMessageBox("Login Successful",message,"information")

	def wrongPassword(self):
		message='''You have entered Wrong Password \n\n Click on FORGOT PASSWORD to Reset Password'''
		ut.showMessageBox("Login Unsuccessful",message,"error")

	def noAccount(self):
		message='''Sorry ,You do not have account \n\n Click on CREATE ACCOUNT'''
		ut.showMessageBox("Login Unsuccesful",message,"warning")

	def isTeacher(self):
		return self.user_type=='teacher'

	def getMailAddress(self):
		if self.user_type=="student":
			return db.getMailAddressOfStudent(self.conn,self.user_id)
		else:
			return db.getMailAddressOfTeacher(self.conn,self.user_id)

	def getLoginTime(self):
		return db.getLoginTime(self.conn,self.user_id,self.user_type)

	def logout(self):
		db.logout(self.conn,self.user_id,self.user_type)

	def getLogoutTime(self):
		return db.getLogoutTime(self.conn,self.user_id,self.user_type)
