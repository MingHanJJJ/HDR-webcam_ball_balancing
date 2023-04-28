import cv2
import numpy as np
from sympy import false


class WebCam:
    cap = None
    def __init__(self) -> None:
        self.cap = self.video_capture()
        pass

    def video_capture(self):
        # Webcamera no 0 is used to capture the frames
        return cv2.VideoCapture(0)
    
    def dectect_boundary(self, pixels, buffer_pixels):
        x_max = y_max = 0
        y_min = len(pixels)
        x_min = len(pixels[0])
        for j in range(len(pixels)): # y
            for i in range(len(pixels[0])): # x
                if(pixels[j][i] == 1):
                    if(self.pixel_buffer_detect(pixels, j, i, buffer_pixels)):
                        x_min = min(x_min, i)
                        x_max = max(x_max, i)
                        y_min = min(y_min, j)
                        y_max = max(y_max, j)
        # print("x min is %s" % x_min)
        # print("x max is %s" % x_max)
        # print("y min is %s" % y_min)
        # print("y max is %s" % y_max)
        
    
    """"
    this function is to make sure all the pixels in the square of corner are in the same color
    """
    def pixel_buffer_detect(self, pixels, y, x, buffer_pixels):
        if((y - buffer_pixels) < 0 or (x - buffer_pixels) < 0 or (x + buffer_pixels) >= len(pixels[0]) or (y + buffer_pixels > len(pixels))):
            return False
        for j in range(-buffer_pixels, buffer_pixels + 1):
            for i in range(-buffer_pixels, buffer_pixels + 1):
                if(pixels[j][i] == 0):
                    return False
        return True

    def start_webcam(self):
        # This drives the program into an infinite loop.
        while(1):        
            # Captures the live stream frame-by-frame
            _, frame = self.cap.read() 
            
            # color select
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110,50,50])
            upper_blue = np.array([130,255,255])
        
            # Here we are defining range of bluecolor in HSV
            # This creates a mask of blue coloured 
            # objects found in the frame.
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            # The bitwise and of the frame and mask is done so 
            # that only the blue coloured objects are highlighted 
            # and stored in res
            # res = cv2.bitwise_and(frame,frame, mask= mask)
            cv2.imshow('frame',frame)
            # cv2.imshow('mask',mask)
            # cv2.imshow('res',res)
            #self.dectect_boundary(mask, 1)
            #print("finished")
            
        
        
            # This displays the frame, mask 
            # and res which we created in 3 separate windows.
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

            
        # Destroys all of the HighGUI windows.
        cv2.destroyAllWindows()
        
        # release the captured frame
        self.cap.release()


if __name__ == "__main__":
    w = WebCam()
    w.start_webcam()


  

  