import pyfiglet
import sys
from select import select
import time
import os
import pandas as pd
import sqlite3

# Modulos y clases creados para el launcher
import utils_launcher.data_scripts as data
from utils_launcher.values import bcolors, size, options
from utils_launcher.values import name_db

def tittle():
    # Logo del launcher
    os.system("clear")
    result = pyfiglet.figlet_format("Launcher")
    print(result)

def main_menu(option):
    # Menu principal del launcher
    if option == 1:
        print(f"{bcolors.BOLD}>> 1. Mostrar scripts en ejecucion.{bcolors.ENDC}")
    else:
        print(">> 1. Mostrar scripts en ejecucion.")

    if option == 2:
        print(f"{bcolors.BOLD}>> 2. Mostrar ultimas peticiones.{bcolors.ENDC}")
    else:
        print(">> 2. Mostrar ultimas peticiones.")

    if option == 3:
        print(f"{bcolors.BOLD}>> 3. Ejecutar/Eliminar script.{bcolors.ENDC}")
    else:
        print(">> 3. Ejecutar/Eliminar script.")

    if option == 4:
        print(f"{bcolors.BOLD}>> 4. Detener el launcher.{bcolors.ENDC}")
    else:
        print(">> 4. Detener el launcher.")

    if option == 4:
        print("\nSaliendo del launcher...")

    if option == options.INVALID:
        print("\nSelect: ", end="")


def scripts_table(scripts):
    # Mostrar los scripts que se estan ejecutando y sus respectivos estados
    while True:
        # Verificamos que los scripts esten corriendo
        for i in range(len(scripts)):
            if not scripts[i].isScriptRunning():
                # Si el script ya no esta corriendo actualizamos la db
                # y lo eliminamos de la lista
                data.update_status(name_db, scripts[i].get_pid(), -1)
                scripts.pop(i)
                break

        tittle() # Launcher logo
        # Columnas
        print("=" * (size.SCRIPTS_TABLE))
        txt = "SCRIPT".center(size.SCRIPT_NAME, " ") + "|" + \
            "PID".center(size.PID, " ") + "|" + \
            "RTSP".center(size.RTSP, " ") + "|" + \
            "STATUS".center(size.STATUS, " ")
        print(txt)
        print("=" * (size.SCRIPTS_TABLE))

        # Leemos la base de datos para conocer el estado actual de los scripts
        # que esta corriendo el launcher
        conn = sqlite3.connect(name_db)
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

            if status == 1:  # El script esta corriendo correctamente
                print(f"{bcolors.OKGREEN}", end="")
                print("Running".center(size.STATUS, " "), end="")
                print(f"{bcolors.ENDC}")

            elif status == -1:  # El script se detuvo
                print(f"{bcolors.FAIL}", end="")
                print("Stopped".center(size.STATUS, " "), end="")
                print(f"{bcolors.ENDC}")

            else:  # El script esta intentando conectarse
                print(f"{bcolors.WARNING}", end="")
                print("Connecting".center(size.STATUS, " "), end="")
                print(f"{bcolors.ENDC}")

            print("-" * (size.SCRIPTS_TABLE))

        conn.close()

        print("\nPara salir presione Enter", end="")
        timeout = 1
        rlist, wlist, xlist = select([sys.stdin], [], [], timeout)
        if rlist:
            break
    
    return scripts

def table_devices(list_devices):
    # Mostrar la informacion que se obtuvo del endpoint

    # Columnas
    print("", flush=True)
    print("=" * size.DEVICES_TABLE)
    txt = "ID".center(size.ID, " ") + "|" + \
        "NAME".center(size.NAME, " ") + "|" + \
        "SCRIPT".center(size.SCRIPT_NAME, " ")
    print(txt)
    print("=" * size.DEVICES_TABLE)

    for i in range(len(list_devices)):
        txt = str(list_devices[i]['id']).center(size.ID, " ") + "|" + \
            list_devices[i]['name'].center(size.NAME, " ") + "|"
        print(txt)
        print("=" * size.DEVICES_TABLE)

    print("")


def filter_input():
    """
    Esta funcion se encarga de filtrar cualquier entrada por teclado que no sea correcta

    Returns:
            option (int): Opcion seleccionada por el usuario
                                      options.INVALID si la opcion no es un int

    """
    try:
        option = int(input())
    except:
        option = options.INVALID

    return option


def transition(option, menu):
    # Realizar una pequena animacion entre cambio de menus"""
    tittle()
    menu(option)
    time.sleep(0.5)


def run_interface(scripts):
    # Interfaz del launcher con el usuario
    option = options.RESTART
   
    tittle()
    main_menu(option)

    option = filter_input()
    if option == options.INVALID or option < options.MAIN1 or option > options.ESCAPE:
        return (True, scripts)  # Opcion incorrecta

    # Realizamos una pequena animacion entre menus
    transition(option, main_menu)

    if option == options.MAIN1:  # Mostramos los scripts que se estan ejecutando
        scripts = scripts_table(scripts)
        return (True, scripts)
    else:
        return (False, scripts)  # Por el momento las demas opciones aun no han sido creadas ##

def close(scripts):
    for i in range(len(scripts)):
        scripts[i].stopScript()
    
    os.system("clear")
