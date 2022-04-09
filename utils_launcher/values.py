from http.client import UNAUTHORIZED
import os

# Colores para imprimir los mensaje que genera la base de datos
#   -Running : Verde -> OKGREEN
#   -Connecting : Amarillo -> WARNING
#   -Stopped : Rojo -> FAIL 
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

# Opciones para la interface
class options:
	ESCAPE = 4 # Salir del menu
	INVALID = -999 # Opcion no valida
	RESTART = -999 # Reset para la opcion. Es necesario al cambiar o iniciar el menu
	MAIN1 = 1 # Menu 1: Mostrar scripts en ejecucion
	MAIN2 = 2 # Menu 2: Mostrar ultimas peticiones 
	MAIN3 = 3 # Menu 3: Ejecutar/Eliminar script

# Medidas de las tablas
class size:
    SCRIPT_NAME = 25
    PID = 7
    RTSP = 67
    STATUS = 14
    MARGIN = 2
    SCRIPTS_TABLE = SCRIPT_NAME + PID + RTSP + STATUS + MARGIN

    ID = 4
    NAME = 22
    DEVICES_TABLE = ID + NAME + SCRIPT_NAME + MARGIN

# Status code errors enviados por el endpoint
class HTTP_ERROR:
    UNAUTHORIZED = 401

# Estados de los scripts
class status:
    RUNNING = 1
    STOPPED = -1
    CONNECTING = 0

dir = 'utils_launcher'
name_db = os.path.join(os.getcwd(), dir, "status_scripts.db") # Nombre de la base de datos
