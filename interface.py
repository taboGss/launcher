import pyfiglet
import sys
from select import select
import time
import os
import pandas as pd
import sqlite3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class options:
	ESCAPE = 4
	INVALID = -999
	RESTART = -999
	MAIN1 = 1
	MAIN2 = 2
	MAIN3 = 3

class size:
	SCRIPT_NAME = 15
	PID = 10
	RTSP = 66
	STATUS = 12
	TOTAL = SCRIPT_NAME + PID + RTSP + STATUS
	MARGIN = 2

def tittle():
	os.system("clear")
	result = pyfiglet.figlet_format("Launcher") # Logo del launcher
	print(result)

def main_menu(option):
	# Esta funcion muestra el menu principal del launcher 

	if option == 1 : 
		print(f"{bcolors.BOLD}>> 1. Mostrar scripts en ejecucion.{bcolors.ENDC}")
	else: 
		print(">> 1. Mostrar scripts en ejecucion.")

	if option == 2 : 
		print(f"{bcolors.BOLD}>> 2. Mostrar ultimas peticiones.{bcolors.ENDC}")
	else: 
		print(">> 2. Mostrar ultimas peticiones.")

	if option == 3 : 
		print(f"{bcolors.BOLD}>> 3. Ejecutar/Eliminar script.{bcolors.ENDC}")
	else: 
		print(">> 3. Ejecutar/Eliminar script.")

	if option == 4 : 
		print(f"{bcolors.BOLD}>> 4. Detener el launcher.{bcolors.ENDC}")
	else: 
		print(">> 4. Detener el launcher.")

	print("\nSelect: ", end="")

def scripts_table():
	# Esta funcion muestra los scripts que se estan ejecutando y 
	# sus respectivos estados

	while True:
		tittle(); 

		# Columnas que se muestran para la funcion scripts_table
		print("=" * (size.TOTAL + size.MARGIN))
		txt = "SCRIPT".center(size.SCRIPT_NAME, " ") + "|" + \
		  	  "PID".center(size.PID, " ") + "|" + \
		  	  "RTSP".center(size.RTSP, " ") + "|" + \
		  	  "STATUS".center(size.STATUS, " ")
		print(txt)
		print("=" * (size.TOTAL + size.MARGIN))

		# Leemos la base de datos para conocer el estado actual de los scripts
		# que esta corriendo el launcher
		conn = sqlite3.connect('status_scripts.db')
		df = pd.read_sql('SELECT * FROM statusScripts', con=conn)

		for i in range(len(df.index)):
			script_name = df['script'][i]
			pid = str(df['pid'][i])
			rtsp = df['rtsp'][i]
			status = df['status'][i]

			txt = script_name.center(size.SCRIPT_NAME, " ") + "|" + \
				  pid.center(size.PID, " ") + "|" + \
				  rtsp.center(size.RTSP, " ") + "|"

			print(txt, end="")
			
			if status == 1: # El script esta corriendo correctamente
				print(f"{bcolors.OKGREEN}", end="")
				print("Running".center(size.STATUS, " "), end="")
				print(f"{bcolors.ENDC}")
		
			elif status == -1: # El script se detuvo
				print(f"{bcolors.FAIL}", end="")
				print("Stopped".center(size.STATUS, " "), end="")
				print(f"{bcolors.ENDC}")
		
			else: # El script esta intentando conectarse
				print(f"{bcolors.WARNING}", end="")
				print("Connecting".center(size.STATUS, " "), end="")
				print(f"{bcolors.ENDC}")
	
			print("-" * (size.TOTAL + size.MARGIN))

		conn.close()

		print("\nPara salir presione Enter", end="")
		timeout = 1
		rlist, wlist, xlist = select([sys.stdin], [], [], timeout)
		if rlist: break

def filter_input():
	"""
	Esta funcion se encarga de filtrar cualquier entrada por teclado que no sea correcta

	Returns:
		option (int): Opcion seleccionada por el usuario
					  options.INVALID si la opcion no es un int

	""" 
	try: option = int(input())
	except: option = options.INVALID

	return option

def transition(option, menu): 
	"""Esta funcion realiza una pequena animacion entre cambio de menus"""
	tittle(); menu(option)
	time.sleep(0.5)

def start_interface():
	# Interfaz del launcher con el usuario 

	option = options.RESTART
	while True:	
		if option == options.ESCAPE: break # Salida de la TUI
	
		tittle()
		main_menu(option)

		option = filter_input()
		if option == options.INVALID or option < options.MAIN1 or option > options.ESCAPE: 
			continue # Opcion incorrecta 
		
		transition(option, main_menu) # Realizamos una pequena animacion entre menus

		if option == options.MAIN1: # Mostramos los scripts que se estan ejecutando
			scripts_table(); option = options.RESTART
		else: 
			break ## Por el momento las demas opciones aun no han sido creadas ##

start_interface()
os.system("clear")
