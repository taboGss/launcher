import os
import time
import requests

# Modulos y clases creados para el launcher
from utils_launcher.values import bcolors
from utils_launcher.process import SubProcess
from utils_launcher.values import name_db  # Path de la base de datos
import utils_launcher.data_scripts as data  # Escribir/Leer la base de datos
import utils_launcher.interface as interface # Terminal User Interface (TUI) del launcher

def get_devices():
    # Entramos al endpoint login para obtener el token de autenticacion
    session = requests.Session()
    pload = {'username': 'javier.rodriguez', 'password': 'secret123'}
    req = session.post('http://192.168.0.135:8000/api/v1/login', data=pload)

    os.system("clear")
    print("Conectando con el EndPoint... ", end="")

    # Verificamos que el servidor fue alcanzado
    if not req:
        raise ConnectionError(
            f"La conexion con login no ha podido ser establecida {req}")

    req_json = req.json()
    if req_json['code'] == 401:  # Credenciales invalidas
        raise ConnectionError(f"Las credenciales son incorrectas")

    # Conexion correcta
    print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")

    headers = {'Authorization': 'Bearer ' + req_json['response']['token']}
    print("Obteniendo info... ", end="")

    # Obtenemos la lista de todos los devices en la DB
    resp = session.get('http://192.168.0.135:8000/api/v1/devices', headers=headers).json()
    list_devices_fromDB = resp['response']
    list_devices = []

    # Obtenemos la informacion que requieren los scripts que van a ser lanzados
    for device in list_devices_fromDB:
        temp_dict = {'id': device['id'],
                     'name': device['name'],
                     'area': device['area']['name'],
                     'rtsp_url': device['rtsp_url'],
                     'rtsp_recording_url': device['rtsp_recording_url']}
        list_devices.append(temp_dict)

    # Dispositivos obtenidos correctamente
    print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
    session.close()

    return list_devices

def launch_scripts(list_devices):
    # Lanzamos los scripts necesarios
    print("Lanzando scripts...")

    # Creamos la DB donde los scripts actualizan su estado
    # Esta es la forma en que la interfaz obtiene la info
    # sobre el estado de los scripts
    data.create_data_base(name_db)

    script_name = "test_detector.py"
    scripts = []
    for i in range(len(list_devices)):
        # Ejecutamos el numero de scripts necesarios
        prss = SubProcess(script_name + " --pos 1 --pos2 1")
        prss.runScript()

        txt = f"{bcolors.BOLD}ID: {bcolors.ENDC}" + str(list_devices[i]['id']) + " " + \
            f"{bcolors.BOLD}NAME: {bcolors.ENDC}" + list_devices[i]['name'] + " " + \
            f"{bcolors.BOLD}SCRIPT: {bcolors.ENDC}" + script_name + " "

        if prss.isScriptRunning():
            # Script lanzado correctamente
            print(txt + f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
            rtsp = list_devices[i]['rtsp_url']
            
            # Cada script debe de conectarse con el servidor para actulizar su estado
            # por eso status = -1 (Stopped)
            data.insertRow(name_db=name_db,
                           script=script_name,
                           pid=prss.get_pid(),
                           rtsp=rtsp,
                           status=-1)

            scripts.append(prss) 
        else:
            print(txt + f"{bcolors.FAIL}FAIL{bcolors.FAIL}")
            scripts.append(None)

        time.sleep(2)
    
    return scripts


# Obtenemos la lista de devices desde el EndPoint
list_devices = get_devices()

# Mostramos los scripts a lanzar
interface.table_devices(list_devices)

# Lanzamos los scripts
scripts = launch_scripts(list_devices)

interface_is_running = True
while interface_is_running:
    # Comunicacion con el usuario a traves de la Terminal User Interface
    interface_is_running, scripts = interface.run_interface(scripts)

# Salimos del launcher, cerramos todos los scripts que se estan ejecuatando
interface.close(scripts)
