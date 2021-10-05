import database as db
import utilities as ut

class Signup:
	def __init__(self,login):
		self.user=login

	def signupAsTeacher(self,user_name,email,contact,password):
		self.user.user_type,self.user.user_name,self.user.user_id=db.signupAsTeacher(self.user.conn,user_name,email,contact,password)
		message='''Account Created Successfully \n\n
		\t\tWelcome '''+user_name
		ut.showMessageBox("Success",message,"information")

	def signupAsStudent(self,user_name,email,contact,password):
		self.user.user_type,self.user.user_name,self.user.user_id=db.signupAsStudent(self.user.conn,user_name,email,contact,password)
		message='''Account Created Successfully \n\n
		\t\tWelcome '''+user_name
		ut.showMessageBox("Success",message,"information")

	def passwordsDoNotMatch(self):
		message='''Passwords do not match \n\n Enter the same Password in both fields'''
		ut.showMessageBox("Password Mismatch",message,"error")

	def hasAccount(self):
		message='''You already have an account in AllInOne'''
		ut.showMessageBox("Account already Present",message,"warning")