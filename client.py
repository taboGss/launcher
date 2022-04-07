import socket
import os
import dataScripts as data

class Client:
	"""Cliente TCP a traves de sockets
	
	Parameters
	----------
	port : int
		Puerto para establecer la conexion con el servidor 
	
	Methods
	-------
	connect_to_server(self)
		Realiza la conexion con el servidor
	send_request(data: str)
		Envia la informacion al servidor
	close(self)
		Cierra el socket TCP
		
	"""

	def __init__(self, port=8080):	
		self.__port = port
		self.__socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.name_db = 'status_scripts.db'
		self.pid = os.getpid()
	
	def connect_to_server(self):
		"""Realiza la conexion con el servidor"""

		# Esperamos hasta que inicie el servidor.
		# En la conexion de sockets con TCP el cliente debe de contactar al
		# servidor (Proceso servidor debe de estar corriendo primero). En 
		# nuestro caso el cliente va estar corriendo primero"""
		while True:
			try:
				self.__socket_client.connect(('localhost', self.__port))
				# Una vez que realizamos la conexion con el servidor
				# actualizamos el status en la db
				data.update_status(self.name_db, self.pid, 1) # Status: running
				break
			except:
				pass

	def send_request(self, data):
		"""Envia la informacion al servidor"""
		data = bytes(data, 'UTF-8')
		self.__socket_client.send(data)
	
	def close(self):
		self.__socket_client.close()
