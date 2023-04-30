from pickletools import int4
from secrets import token_bytes
import serial

class Serial_port:
    port = None
    def __init__(self) -> None:
        self.port = serial.Serial(port="COM1", baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    
    def send_boundary(self):
        pass

    def send_poition(self, x:int, y:int):
        x_byte = x.to_bytes(1, 'little')
        y_byte = y.to_bytes(1, 'little')
        
        """
        the write function have the start bit (which is always 0), the data bits (in this case, one or two bytes representing the integer)
        , and the stop bit (which is always 1) to create a complete data  
        """
        self.port.write(x)
        self.port.write(y)

    def close(self):
        self.port.close()
