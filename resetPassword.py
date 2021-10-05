import database as db
import utilities as ut

class ResetPassword:
	def __init__(self,login):
		self.user=login

	def resetPassword(self,mail,password,user_type):
		db.updatePassword(self.user.conn,mail,password,user_type)

	def checkNewUser(self,mail):
		user_type,user_id=db.checkStudentOrTeacher(self.user.conn,mail)
		return user_type

	def noAccount(self):
		message='''Sorry, You do not have account \n\n Click on CREATE ACCOUNT'''
		ut.showMessageBox("No Account",message,"warning")

	def passwordsDoNotMatch(self):
		message='''Passwords do not match \n\n Enter the same Password in both fields'''
		ut.showMessageBox("Password Mismatch",message,"error")

	def passwordUpdated(self):
		message='''Password Updated Successfully \n\n Kindly Login with the New Password'''
		ut.showMessageBox("Password Updated",message,"information")