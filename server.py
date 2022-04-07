import socket
import threading

class ThreadServer(threading.Thread):
	"""Clase para crear los sockets usando hilos
	
	Attributes
	----------
	connection : socket
		Socket creado por la clase Server
	address : int
		numero de socket
	headers : dictionary
		headers para acceder a la API
	
	Methods
	-------
	run(self)
		funcion que lee la informacion enviada por el cliente
		y realiza la peticion

	"""
	def __init__(self, connection, address, headers):
		threading.Thread.__init__(self)
		
		self.connection = connection
		self.address = address
		self.headers = headers

	def run(self):
		# Esta funcion es la encargada de recibir la informacion de
		# su cliente correspodiente y relizar la accion necesaria	
		#print(f'Conexion establecida con script {self.address}') # Conexion establecida
		
		while True:
			# Recibimos la solicitud del cliente
			request = self.connection.recv(2048).decode()
			if request == "": continue
			print(request)

threads = [] # Arreglo para guardar los hilos
port = 8080 # Listener en el puerto 8080
address = 0 # Numero de scripts corriendo
headers = ""

# Creamos un socket para leer las peticiones de escritura de cada
# script en la DB
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind(('localhost', port)) 
socket_server.listen(5)

while True:
	# Creamos la conexion con cada cliente una a la vez
	connection, _ = socket_server.accept()
	thread_server = ThreadServer(connection, address, headers)
	address += 1
			
	thread_server.start()
	threads.append(thread_server)


