import os
import dataScripts as data

name_db = 'status_scripts.db'
pid = os.getpid()

def connect_to_launcher():
	""" Actulizar el estado del script a RUNNING"""
	data.update_status(name_db, pid, 1) # Status: running


