from datetime import datetime,date,timedelta
import tkinter as tk
from tkinter import simpledialog,messagebox
import string
import random
import smtplib
from email.message import EmailMessage

mailAddress=<email_address>
password=<password>

def getCharFromNum(n):
	d=96+max(1,n%26)
	return chr(d)

def generateCode():
	lengths=[6,7,8,9]
	length=random.choice(lengths)
	code="".join(random.choices(string.ascii_letters+string.digits,k=length))
	return code

def getCurrentTime():
	return datetime.strptime(datetime.strftime(datetime.now(),"%d-%m-%Y %H:%M:%S"),"%d-%m-%Y %H:%M:%S")

def createDatetime(deadline):
	return datetime.strptime(deadline,"%Y-%m-%d %H:%M")

def createDatetime2(deadline):
	return datetime.strptime(deadline,"%Y-%m-%d %H:%M:%S")

def dialogForOtp():
	root=tk.Tk()
	enteredOTP=0
	root.withdraw()
	enteredOTP = simpledialog.askinteger(title="OTP",prompt="Enter the Received OTP : ")
	root.destroy()
	return enteredOTP

def dialogForCode():
	root=tk.Tk()
	code=None
	root.withdraw()
	code = simpledialog.askstring(title="Class Code",prompt="Enter the Subject Code : ")
	root.destroy()
	return code

def askQuestion(title,message):
	root=tk.Tk()
	root.withdraw()
	res=messagebox.askquestion(title,message)
	root.destroy()
	return res == 'yes'

def showMessageBox(title,message,message_type):
	root=tk.Tk()
	root.withdraw()

	if message_type == "warning":
		messagebox.showwarning(title,message)

	elif message_type == "information":
		messagebox.showinfo(title,message)

	elif message_type == "error":
		messagebox.showerror(title,message)

	root.destroy()

def checkEquality(value1,value2):
	return value1==value2

def getColors(length):
	colors=['static/blue.jpeg','static/red.jpg','static/green.jpg',
	'static/darkred.jpeg','static/yellowgreen.jpg','static/skyblue.jpeg',
	'static/orangered.jpg','static/cfblue.jpg','static/black.jpg']
	return random.choices(colors,k=length)

def getServer():
	server=smtplib.SMTP_SSL("smtp.gmail.com",465)
	server.login(mailAddress,password)
	server.ehlo()
	return server

def sendMail(ToAddress,body,subject):
	server=getServer()

	message=EmailMessage()

	message.set_content(body)
	message['Subject'] = subject
	message['From'] = mailAddress
	message['To'] = ", ".join(ToAddress)

	server.send_message(message)

	server.close()

def convertTuplesToList(data):
	return list(map(lambda x:x[0],data))

def sendSuccessfulEnrollmentMail(ToAddress,subject_name,user_name,teacher_name):
	subject = "ENROLLED SUCCESSFULLY"
	body = '''Hello {},\n\n\t\t
	You have been Successfully Enrolled in the Course : \n\t{}\n
	which is Handled By {}'''.format(user_name,subject_name,teacher_name)

	sendMail([ToAddress],body,subject)

def newTestMail(ToAddress,subject_name,teacher_name,deadline,marks):
	ToAddress=convertTuplesToList(ToAddress)

	subject = "NEW TEST POSTED"
	body = '''Hello,\n\n\t\t
	New Test has been Posted in the Classroom: \n\t {}\n
	by {}. \n\n Deadline : {} \n\n Marks : {}'''.format(subject_name,teacher_name,deadline,marks)

	sendMail(ToAddress,body,subject)

def newAssignmentMail(ToAddress,subject_name,teacher_name,deadline):
	ToAddress=convertTuplesToList(ToAddress)

	subject = "NEW ASSIGNMENT POSTED"
	body = '''Hello,\n\n\t\t
	New Assignment has been Posted in the Classroom: \n\t {}\n
	by {}. \n\n Deadline : {}'''.format(subject_name,teacher_name,deadline)

	sendMail(ToAddress,body,subject)

def newNotesMail(ToAddress,subject_name,teacher_name):
	ToAddress=convertTuplesToList(ToAddress)

	subject = "NEW NOTES UPLOADED"
	body = '''Hello,\n\n\t\t
	New Notes has been Uploaded in the Classroom: \n\t {}\n
	by {}.'''.format(subject_name,teacher_name)

	sendMail(ToAddress,body,subject)

def getDifference(datetime1,datetime2):
	datetime2 = createDatetime2(datetime2)
	td=datetime1 - datetime2
	hours = td.seconds//3600
	mins = (td.seconds % 3600) // 60
	return hours,mins
