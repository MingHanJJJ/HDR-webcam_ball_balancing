import cv2
import numpy as np
import serial_port


class WebCam:
    cap = None
    def __init__(self) -> None:
        self.cap = self.video_capture()
        pass

    def video_capture(self):
        # Webcamera no 0 is used to capture the frames
        return cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
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
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret , thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            rects = []
            max_w = 0
            max_h = 0
            for contour in contours:
                x,y,w,h = cv2.boundingRect(contour)
                max_w = max(max_w, w)
                max_h = max(max_h, h)
                rects.append((x,y,w,h))
            print(len(rects))
            print("max w: %s, max h: %s" % (max_w, max_h))

            cv2.imshow('frame',frame)             
        
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


  

  