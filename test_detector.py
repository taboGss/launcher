import argparse
import cv2
import client

def move():
	client.connect_to_launcher()
	
	img = cv2.imread('lenna.jpg')
	cv2.imshow('image', img)
	cv2.waitKey(0)

	cv2.destroyAllWindows()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--rtsp', type=str, default="", help='position')
	parser.add_argument('--id', type=str, default="", help='position2')
	opt = parser.parse_args()

	move()
