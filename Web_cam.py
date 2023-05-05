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
        return cv2.VideoCapture(1, cv2.CAP_DSHOW)
    
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
        dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2
        prevCircle = None 
        chosen = [0,0]
        serial = serial_port.Serial_port()

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
            rect_x = 0
            rect_y = 0
            for contour in contours:
                x,y,w,h = cv2.boundingRect(contour)
                if(max_w < w): 
                    max_w = max(max_w, w)
                    max_h = max(max_h, h)
                    rect_x = x
                    rect_y = y
                rects.append((x,y,w,h))

            # print("x:%s  y:%s" % (rect_x, rect_y))
            # print("max w: %s, max h: %s" % (max_w, max_h))
            frame = cv2.circle(frame, (rect_x, rect_y), radius=10, color=(0, 0, 255), thickness=-1)
            frame = cv2.circle(frame, (rect_x + max_w, rect_y), radius=10, color=(0, 0, 255), thickness=-1)
            frame = cv2.circle(frame, (rect_x + max_w, rect_y + max_h), radius=10, color=(0, 0, 255), thickness=-1)
            frame = cv2.circle(frame, (rect_x, rect_y + max_h), radius=10, color=(0, 0, 255), thickness=-1)

            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurFrame = cv2.GaussianBlur(grayFrame, (17, 17), 0)
            circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 0.5, 100, param1=100, param2=30, minRadius=10, maxRadius=50) 
            if circles is not None:
                circles = np.uint16(np.around(circles))
                chosen = None
                for i in circles[0, :]:
                    if chosen is None:
                        chosen = i
                    if prevCircle is not None:
                        if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                            chosen = i
                #chosen[0], chosen[1] are x, y coordinations; chosen[2] represents the radius of circle that cv.circle() is drawing
                cv2.circle(frame, (chosen[0], chosen[1]), 1, (0, 100, 100), 3)
                cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)

                #print(f"Center of the circle: ({chosen[0]}, {chosen[1]})")
                prevCircle = chosen

            

            ##############
            cv2.imshow('frame',frame)   
            
            serial.send_poition((chosen[0].item()), (chosen[1].item()))          
        
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


  

  