import argparse
import client
import cv2


def main():
    
   # client.connect_to_launcher()
   
   img = cv2.imread('lenna.jpg')
   cv2.imshow(str(client.pid), img3)
   cv2.waitKey(0)

   cv2.destroyAllWindows()
   # client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rtsp', type=str, default="", help='position')
    parser.add_argument('--id', type=str, default="", help='position2')
    opt = parser.parse_args()

    main()
