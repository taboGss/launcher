"""Modulo lanzador de aplicaciones

Usage:
    1. Configurar el archivo ./cfg/launcher_cfg.json
        - script_name : script a lanzar
        - params : parametros solicitados por el script
        - set_params : Si el script necesita algun parametro fijo, 
            fijarlo en esta seccion
        - alias : Si el endpoint arroja un parametro con algun nombre
            diferente, especificarlo 
    
    2. Establecer los parametros USER, PASSWORD y endpoint en el modulo
       ./utils_launcher/credentials.py
"""
import os
import time

import requests
import json

from utils_launcher.values import bcolors
from utils_launcher.process import SubProcess
from utils_launcher.values import status as status_script
from utils_launcher.values import HTTP_ERROR
from utils_launcher.credentials import USERNAME, PASSWORD, endpoint
from utils_launcher.values import name_db # Path de la base de datos
import utils_launcher.data_scripts as data  # Escribir/Leer la base de datos
import utils_launcher.interface as interface # Terminal User Interface (TUI) 


def read_launcher_cfg(list_devices): 
    # Parametros de configuracion que entrega el endpoint 
    params_endpoint = list_devices[0].keys()
    
    # Configuracion de parametros que enviara el launcher a cada script
    file = open('cfg/launcher_cfg.json') 
    cfg_json = json.load(file)
    file.close()

    # Parametros que reciben un valor predefinido
    set_params = cfg_json['set_params'].keys()
    # Parametros que el endpoint entrega con otro nombre
    alias = cfg_json['alias'].keys()

    cfg = []
    for i in range(len(list_devices)):
        script_cfg = {}
        params = ""
        script_cfg['script_name'] = cfg_json['script_name']

        # Iteramos entre todos los parametros solicitados por el script 
        # en el archivo launcher_cfg.json
        for param in cfg_json['params']:
            params += " --" + param + " "

            # El parametro solicitado si es entregado por el endpoint
            if param in params_endpoint:
                # El parametro esta marcado como set en el .json
                if param in set_params:
                    params += cfg_json['set_params'][param]
                else:
                    # El parametro es arbitrario. Lo tomamos del endpoint
                    params += list_devices[i][param] 
            
            elif param in set_params:
                # El parametro no es entregado por el endpoint, pero esta
                # marcado como set en el .json
                params += cfg_json['set_params'][param]
               
            elif param in alias:
                # El endpoint entrega el parametro, pero con un nombre
                # diferente al solicitado por el script
                params += list_devices[i][cfg_json['alias'][param]]
            
            else:
                # Por cada parametro que no encuentre regresa None
                params += "None"

        script_cfg['params'] = params
        cfg.append(script_cfg)
    
    return cfg


def get_devices():
    # Entramos al endpoint login para obtener el token de autenticacion
    os.system("clear")
    print("Conectando con el EndPoint... ", end="", flush=True)

    session = requests.Session()
    pload = {'username': USERNAME, 'password': PASSWORD}
    req = session.post(endpoint.LOGIN, data=pload)

    # Verificamos que el servidor fue alcanzado
    if not req:
        raise ConnectionError(
            f"La conexion con login no ha podido ser establecida {req}")

    req_json = req.json()
    if req_json['code'] == HTTP_ERROR.UNAUTHORIZED:
        raise ConnectionError(f"Las credenciales son incorrectas")

    # Conexion correcta
    print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")

    headers = {'Authorization': 'Bearer ' + req_json['response']['token']}
    print("Obteniendo info... ", end="")

    # Obtenemos la lista de todos los devices en el EndPoint
    resp = session.get('http://192.168.0.135:8000/api/v1/devices', 
                        headers=headers).json()
    list_devices_fromDB = resp['response']
    list_devices = []

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
    print("Lanzando scripts...")

    # Creamos la DB donde los scripts actualizan su estado. Esta es la forma 
    # en que la interfaz obtiene la info sobre el estado de los scripts
    data.create_data_base(name_db)

    # Leemos la configuracion del launcher -- cfg/launcher_cfg.json
    cfg_scripts = read_launcher_cfg(list_devices)
    scripts = []
    
    num_devices = 1 # Para hacer test. Numero de scripts que queremos correr

    #for i in range(len(list_devices)):
    for i in range(num_devices):
        prss = SubProcess(cfg_scripts[i]['script_name'] 
                          + cfg_scripts[i]['params'])
        prss.runScript()

        txt = f"{bcolors.BOLD}ID: {bcolors.ENDC}" \
                 + str(list_devices[i]['id']) + " " \
                 + f"{bcolors.BOLD}NAME: {bcolors.ENDC}" \
                 + list_devices[i]['name'] + " " \
                 + f"{bcolors.BOLD}SCRIPT: {bcolors.ENDC}" \
                 + cfg_scripts[i]['script_name'] + " "

        if prss.isScriptRunning():
            print(txt + f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
            params = cfg_scripts[i]['params']
            list_params = params.split()
            
            # Obtenemos el rtsp de cada script
            for i in range(len(list_params)):
                if list_params[i] == "--rtsp":
                    rtsp = list_params[i + 1] 
                    break

            # Cada script debe de conectarse con el servidor para actulizar 
            # su estado. Por eso status = Stopped
            data.insertRow(name_db=name_db,
                           script=cfg_scripts[i]['script_name'],
                           pid=prss.get_pid(),
                           rtsp=rtsp,
                           status=status_script.STOPPED)

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
