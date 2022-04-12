import numpy as np
import cv2

class Screen:
    def __init__(self, shape):
        self.shape = shape
        self.no_signal = np.zeros(self.shape, dtype='uint8')
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (50, 50)
        self.fontScale = 2
        self.color = (255, 255, 255)
        self.thickness = 3

        self.no_signal = cv2.putText(self.no_signal, 'NO SIGNAL', self.org, 
                                     self.font, self.fontScale, self.color, self.thickness,
                                     cv2.LINE_AA)