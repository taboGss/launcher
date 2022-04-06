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

class Server:
	"""Clase Servidor. Crea los sockets multihilo para poder manejar
	   diferentes clientes
	
	Methods
	-------
	start(headers: dictionary)
		Incia el servidor
		
	"""
	def __init__(self):
		self.threads = [] # Arreglo para guardar los hilos
		self.port = 8080 # Listener en el puerto 8080
		self.address = 0 # Numero de scripts corriendo

		# Creamos un socket para leer las peticiones de escritura de cada
		# script en la DB
		self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_server.bind(('localhost', self.port)) 
		self.socket_server.listen(5)

	def acccept_connection(self, headers):
			# Creamos la conexion con cada cliente una a la vez
			connection, _ = self.socket_server.accept()
			thread_server = ThreadServer(connection, self.address, headers)
			self.address += 1
			
			thread_server.start()
			self.threads.append(thread_server)


