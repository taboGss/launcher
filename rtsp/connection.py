import cv2


class cam_rtsp:
    """Interface para conexion rtsp

    Parameters
    -----------
    uri : string
        Direccion rtsp de la camara.

    Attributes
    -----------
    cap : VideoCapture (OpenCV)
        Objeto VideoCapture de OpenCV.
    status : boolean
        Estado de la camara despues de leer un frame. 
    frame : numpy-array (OpenCV)
        Frame leido desde rtsp 
    """
    def __init__(self, uri):
        self.uri = uri
        self.cap = cv2.VideoCapture(uri)
        self.status, self.frame = self.cap.read()

        if not self.cap.isOpened():
            raise ConnectionRefusedError(f'Error. La camara {self.uri} \
                                           no es accesible')

    def read(self):
        """Leer un frame desde la camara rtsp

        Returns
        -------
        frame : numpy-array (OpenCV)
        """

        frame = self.frame.copy()

        try:
            self.status, self.frame = self.cap.read()
        except:
            self.status = False

        return frame

    def reconnect_cam(self):
        """Restablecer la conexion con la fuente rtsp."""
        self.cap.release()
        self.cap = cv2.VideoCapture(self.uri)
        
        if self.cap.isOpened():
            self.status, self.frame = self.cap.read()
    
    def release(self):
        """Funcion release como en OpenCV."""
        self.cap.release()

    def is_online(self): 
        """Revisar el status de la conexion rtsp 
        
        Si la conexion es valida return True en otro caso return False
        """
        return self.status
    