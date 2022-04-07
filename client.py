import os
import dataScripts as data

class Client:
	def __init__(self):	
		self.name_db = 'status_scripts.db'
		self.pid = os.getpid()
	
	def connect_to_server(self):
		data.update_status(self.name_db, self.pid, 1) # Status: running
	
	def close(self):
		pass
