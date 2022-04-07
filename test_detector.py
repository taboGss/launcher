import argparse
import cv2
import client

def move():
	client.connect_to_launcher()
	
	img = cv2.imread('/home/tabo/Desktop/lenna.jpg')
	cv2.imshow('image', img)
	cv2.waitKey(0)

	cv2.destroyAllWindows()
	client.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--pos', type=int, default=0, help='position')
	parser.add_argument('--pos2', type=int, default=0, help='position2')
	opt = parser.parse_args()

	move()
