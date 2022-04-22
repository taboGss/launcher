"""Modulo cliente para establecer conexion con el launcher

	Methods
	-------
	connect_to_launcher()
		Actualiza el estado del script y obtiene los headers para 
		interactuar con el endpoint
	connecting_rtsp()
		Establece el estado del script a CONNECTING
	connected_rtsp()
		Restablece el estado del script a RUNNING
"""
import os

import requests
import json

import utils_launcher.data_scripts as data
from utils_launcher.values import name_db, status, HTTP_ERROR
from utils_launcher.credentials import USERNAME, PASSWORD, endpoint


# Obtenemos el process identification number (PID) del script que invoco 
# al cliente.El PID es la forma en la que Launcher distingue todos los 
# scripts que se estan corriendo   
pid = os.getpid()
headers = {}
session = requests.Session() 

# Tipos de scripts 
SPEED = 0
PERSONS = 1


def connect_to_launcher():
	"""Actulizar el estado del script a RUNNING y obtiene los headers"""
	pload = {'username': USERNAME, 'password': PASSWORD}
	req = session.post(endpoint.LOGIN, data=pload)

	# Verificamos que el servidor fue alcanzado
	if not req:
		raise ConnectionError(f"La conexion con login no ha podido \
								ser establecida {req}")

	req_json = req.json()
	if req_json['code'] == HTTP_ERROR.UNAUTHORIZED:
		raise ConnectionError(f"Las credenciales son incorrectas")

	headers['Authorization']  = 'Bearer ' + req_json['response']['token']
	data.update_status(name_db, pid, status.RUNNING)


def get_endpoint_template(script_type):
	"""Obtener los datos necesarios para hacer Post
	
	Returns
	-------
	template : dict
		template para rellenar y enviar al EndPoint
	"""
	if script_type == SPEED:
		file = open('cfg/speed_cfg.json') 
		cfg_json = json.load(file)
		file.close()
	else:
		cfg_json = {"Empty": None} # Aqui va lo de Angel. Aun no esta listo

	template = {}
	for key in cfg_json:
		template[key] = None
	
	return template


def post_update(data, script_type):
	"""Actualizar datos en el EndPoint

	Parameters
	----------
	data : dict
		template con los datos actualizados
	script_type : int
		tipo de script (SPEED / PERSONS)
	
	Returns
	-------
	status : bool
		Se realizo exitosamente el update : True
		otherwise : False
	"""
	if script_type == SPEED:
		req = session.post(endpoint.POST_SPEED,
						   json=data,
						   headers=headers)
	else:
		pass # Aqui va lo de Angel. Aun no esta listo

	return True


def connecting_rtsp():
	data.update_status(name_db, pid, status.CONNECTING)


def connected_rtsp():
	data.update_status(name_db, pid, status.RUNNING)


def close():
	session.close()


