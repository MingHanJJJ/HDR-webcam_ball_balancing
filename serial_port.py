from pickletools import int4
from secrets import token_bytes
import time
import serial

class Serial_port:
    port = None
    def __init__(self) -> None:
        self.port = serial.Serial(port="COM4", baudrate=9600, timeout=1)
        
    
    def send_boundary(self):
        pass

    def send_poition(self, x:int, y:int):
        x_byte = x.to_bytes(2, 'big')
        y_byte = y.to_bytes(2, 'big')
        """
        the write function have the start bit (which is always 0), the data bits (in this case, one or two bytes representing the integer)
        , and the stop bit (which is always 1) to create a complete data  
        """
        
        self.port.write(x_byte)
        self.port.write(y_byte)

    def close(self):
        self.port.close()

if __name__ == "__main__":
    sr = Serial_port()
    while(1):
        # sr.send_poition(612,535)
        crc = 32678
        sr.port.write(crc.to_bytes(2, 'big'))
        print("send")
        time.sleep(1) 


  

  