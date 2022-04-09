""" Este es un intento de un docstring """

import os
import requests
import utils_launcher.data_scripts as data
from utils_launcher.values import name_db, status, HTTP_ERROR
from utils_launcher.credentials import USERNAME, PASSWORD, endpoint

# Obtenemos el process identification number (PID) del script que invoco al cliente.
# El PID es la forma en la que Launcher distingue todos los scripts que se 
# estan corriendo   
pid = os.getpid()

session = requests.Session() 
headers = {}

def connect_to_launcher():
	"""Actulizar el estado del script a RUNNING y obtiene los headers"""
	pload = {'username': USERNAME, 'password': PASSWORD}
	req = session.post(endpoint.LOGIN, data=pload)

	# Verificamos que el servidor fue alcanzado
	if not req:
		raise ConnectionError(f"La conexion con login no ha podido ser establecida {req}")

	req_json = req.json()
	if req_json['code'] == HTTP_ERROR.UNAUTHORIZED: # Credenciales invalidas
		raise ConnectionError(f"Las credenciales son incorrectas")

	headers['Authorization']  = 'Bearer ' + req_json['response']['token']
	data.update_status(name_db, pid, status.RUNNING)


def update_params(coordinate_x, coordinate_y, temp):
	"""Post EndPoint"""

	data = {"device_id": 3,
			"coordinates": [{"x": coordinate_x,
							 "y": coordinate_y,
							 "temp": temp}]}
	
	req = session.post("http://192.168.0.135:8000/api/v1/device-coord",
					   json=data,
					   headers=headers)

def connecting_rtsp():
	data.update_status(name_db, pid, status.CONNECTING)

def close():
	session.close()


