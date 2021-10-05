import database as db
import sqlite3

class Database:
	def __init__(self,database):
		self.database=database
		self.conn=None

	def connect(self):
		self.conn=sqlite3.connect(self.database,check_same_thread=False)
		self.conn.execute("PRAGMA foreign_keys = ON")

	def createTables(self):
		#while running for the first time
		db.createTables(self.conn)