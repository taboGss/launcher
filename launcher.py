"""Modulo lanzador de aplicaciones

Usage:
    1. Configurar el archivo ./cfg/launcher_cfg_... .json
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
import argparse
import json

from utils_launcher.values import bcolors
from utils_launcher.values import list_scripts
from utils_launcher.process import SubProcess
from utils_launcher.values import status as status_script
from utils_launcher.values import HTTP_ERROR
from utils_launcher.credentials import USERNAME, PASSWORD, endpoint, id
from utils_launcher.values import name_db # Path de la base de datos
import utils_launcher.data_scripts as data  # Escribir/Leer la base de datos
import utils_launcher.interface as interface # Terminal User Interface (TUI) 


def read_launcher_cfg(list_devices, id_script): 
    # Parametros de configuracion que entrega el endpoint 
    params_endpoint = list_devices[0].keys()
    
    # Configuracion de parametros que enviara el launcher a cada script
    if id_script == id.SPEED:
        file = open('cfg/launcher_cfg_speed.json')
    elif id_script == id.PERSONS:
        file = open('cfg/launcher_cfg_persons.json')

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
                    if not isinstance(cfg_json['set_params'][param], str):
                        params += str(cfg_json['set_params'][param])
                    else:
                        params += cfg_json['set_params'][param]
                else:
                    # El parametro es arbitrario. Lo tomamos del endpoint
                    if not isinstance(list_devices[i][param], str):
                        params += str(list_devices[i][param])
                    else:
                        params += list_devices[i][param] 
            
            elif param in set_params:
                # El parametro no es entregado por el endpoint, pero esta
                # marcado como set en el .json
                if not isinstance(cfg_json['set_params'][param], str):
                    params += str(cfg_json['set_params'][param])
                else:
                    params += cfg_json['set_params'][param]
               
            elif param in alias:
                # El endpoint entrega el parametro, pero con un nombre
                # diferente al solicitado por el script
                if not isinstance(list_devices[i][cfg_json['alias'][param]],
                                  str):
                    params += str(list_devices[i][cfg_json['alias'][param]])
                else:
                    params += list_devices[i][cfg_json['alias'][param]]
            
            else:
                # Por cada parametro que no encuentre regresa None
                params += "None"

        script_cfg['params'] = params
        cfg.append(script_cfg)
    
    return cfg


def format_coordinates(coordinates):
	"""Dar formato a las coordenadas que provienen del Endpoint"""
	coor = "["
	for point in coordinates:
		coor += "(" + str(point['x']) + "," + str(point['y']) + "),"	
	
	return coor[:-1] + "]"


def get_devices(id_script):
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
    resp = session.get(endpoint.GET_DEVICES, headers=headers).json()
    list_devices_from_endpoint = resp['response']
    list_devices = []

    for device in list_devices_from_endpoint:
        temp_dict = {'id': device['id'],
                     'name': device['name'],
                     'area': device['area']['name'],
                     'rtsp_url': device['rtsp_url'],
                     'rtsp_recording_url': device['rtsp_recording_url'],
                     'zones' : '',
                     'zones_id' : ''}
        list_devices.append(temp_dict)

    ### TEMPORAL ###
    #list_devices = [list_devices[0]]

    # Obtenemos las zonas por cada camara
    body = {'event_type_id' : id_script} 
    for idx, device in enumerate(list_devices):
        resp = session.get(endpoint.GET_DEVICES_ZONES + str(device['id']), 
                           data=body,
                           headers=headers).json()
        
        zones = resp['response']['zones']
        zones_str = "\'[" # Formato propuesto por Angel
        zones_id_str = "\'[" # Formato propuesto por Angel
        
        for zone in zones:
            zones_str += format_coordinates(zone['coordinates']) + ","
            zones_id_str += str(zone['id']) + ","
        
        zones_str = zones_str[:-1] + "]\'"
        zones_id_str = zones_id_str[:-1] + "]\'"

        list_devices[idx]['zones'] = zones_str
        list_devices[idx]['zones_id'] = zones_id_str
        
    # Dispositivos obtenidos correctamente
    print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
    session.close()

    return list_devices


def launch_scripts(list_devices, id_script):
    print("Lanzando scripts...")

    # Creamos la DB donde los scripts actualizan su estado. Esta es la forma 
    # en que la interfaz obtiene la info sobre el estado de los scripts
    data.create_data_base(name_db)

    # Leemos la configuracion del launcher -- cfg/launcher_cfg.json
    cfg_scripts = read_launcher_cfg(list_devices, id_script)
    scripts = []
    
    for i in range(len(list_devices)):
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
            for j in range(len(list_params)):
                if list_params[j] == "--rtsp":
                    rtsp = list_params[j + 1] 
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

def main():
    script_to_launch = opt.script
    # El endpoint entrega las zonas de cada camara de acuerdo al id  
    # especifico de cada aplicacion
    if script_to_launch == list_scripts.SPEED:
        id_script = id.SPEED 
    else: 
        id_script = id.PERSONS
    
    # Obtenemos la lista de devices desde el EndPoint
    list_devices = get_devices(id_script)

    # Mostramos los scripts a lanzar
    interface.table_devices(list_devices)

    # Lanzamos los scripts
    scripts = launch_scripts(list_devices, id_script)

    interface_is_running = True
    while interface_is_running:
        # Comunicacion con el usuario a traves de la Terminal User Interface
        interface_is_running, scripts = interface.run_interface(scripts)

    # Salimos del launcher, cerramos todos los scripts que se 
    # estan ejecuatando
    interface.close(scripts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--script', type=str, required=True, 
                        help='Tipo de script [persons, speed]')

    opt = parser.parse_args()
    main()
