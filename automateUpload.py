from selenium import webdriver

class Automate:
	def __init__(self):
		self.driver=webdriver.Chrome('static/chromedriver')

	def goToGoogleDrive(self):
		driver.get('https://drive.google.com')	

	def uploadFiles(self,files):
