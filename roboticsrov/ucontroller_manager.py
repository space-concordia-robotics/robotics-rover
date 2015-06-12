
import serial
import sys

class SerialConnection:
    serial_conn = None

    # Initiliaze all variables
    def __init__(self,
                 bps=9600,
                 port='/dev/ttyACM0',
                 timeout=5,
                 parity=serial.PARITY_EVEN,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS):

        self.serial_conn = serial.Serial()
        self.serial_conn.baudrate = bps
        self.serial_conn.port = port
        self.serial_conn.timeout = timeout
        self.serial_conn.parity = parity
        self.serial_conn.stopbits = stopbits
        self.serial_conn.bytesize = bytesize

    def openConn(self):
        return self.serial_conn.open()

    def checkConn(self):
        return self.serial_conn.isOpen()

    def closeConn(self):
        return self.serial_conn.close()

    def write(self, character):
        self.serial_conn.write(character)

    def readline(self, numbytes):
        return self.serial_conn.readline(numbytes)

class UControllerManager:
    serial_conn = {'parent_board': None,
                   'left_motors': None,
                   'right_motors': None}

    # Create the serial connections we need
    def __init__(self):
        self.serial_conn['parent_board'] = SerialConnection()
     #   self.serial_conn['left_motors'] = SerialConnection(port=None)
     #   self.serial_conn['right_motors'] = SerialConnection(port=None)

        # Try to open the connections
        self.serial_conn['parent_board'].openConn()
     #   self.serial_conn['left_motors'].openConn()
     #   self.serial_conn['right_motors'].openConn()

        if not self.serial_conn['parent_board'].checkConn():
            sys.exit("Failed opening parent_board serial connection.")

     #   if not self.serial_conn['left_motors'].checkConn():
     #       sys.exit("Failed opening left_motors serial connection.")

     #   if not self.serial_conn['right_motors'].checkConn():
     #       sys.exit("Failed opening right_motors serial connection.")

    def run(self):
       
        if self.serial_conn['parent_board'].checkConn():
            x = 0
            while x<10:
                # Send one byte.
                self.serial_conn['parent_board'].write(chr(x)) 
                # Read one byte.
                val = self.serial_conn['parent_board'].readline(1)
                print val
                x += 1

        self.closeConnections()


    def closeConnections(self):
        # Close all connections
        self.serial_conn['parent_board'].closeConn()
     #   self.serial_conn['left_motors'].closeConn()
     #   self.serial_conn['right_motors'].closeConn()
            

