import argparse
import cv2
import client

from rtsp.auxiliar_functions import Screen
from rtsp.connection import cam_rtsp

def main():
    # Lo primero que hay que hacer es subscribirse al launcher. Con esto
    # el launcher sabe que el script esta corriendo correctamente y obtiene
    # las credenciales para subir y bajar informacion del end point
    client.connect_to_launcher()
    _, rtsp = opt.id, opt.rtsp

    # Abrimos la conexion rtsp a traves del modulo cam_rtsp
    cap = cam_rtsp(rtsp)
    cv2.namedWindow(rtsp, cv2.WINDOW_NORMAL)
    screen = Screen(cap.frame.shape)

    while True:
        if not cap.is_online():  # Verificamos que la conexion rtsp este activa
            client.connecting_rtsp()  # Avisamos al launcher que perdimos la conexion

            while not cap.is_online():
                cv2.imshow(rtsp, screen.no_signal)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                cap.reconnect_cam()  # Intenetamos reconectar con el rtsp antes de seguir procesando

            client.connected_rtsp()  # Avisamos al launcher que recuperamos la conexion

        ### Se realiza todo el procesamiento requerido ###
        frame = cap.read()
        cv2.imshow(rtsp, frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rtsp', type=str, default="", help='position')
    parser.add_argument('--id', type=str, default="", help='position2')
    opt = parser.parse_args()

    main()
