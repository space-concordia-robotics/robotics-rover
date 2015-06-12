import serial
import sys

class UControllerManager:
    ucontr_conn = None

    # Create the serial connections we need
    def __init__(self,
                 bps=9600,
                 port='/dev/ttyACM0',
                 timeout=1,
                 parity=serial.PARITY_EVEN,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS):

        self.ucontr_conn = serial.Serial()
        self.ucontr_conn.baudrate = bps
        self.ucontr_conn.port = port
        self.ucontr_conn.timeout = timeout
        self.ucontr_conn.parity = parity
        self.ucontr_conn.stopbits = stopbits
        self.ucontr_conn.bytesize = bytesize

    def run(self):
        # Try to open the connections
        self.ucontr_conn.open()

        if not self.ucontr_conn.isOpen():
            sys.exit("Failed opening serial connection for ucontroller.")
        else:
            # Start of main loop.
            print "Main loop running."
            x = 0
            while x<10:
                # Send one byte.
                self.ucontr_conn.write(chr(x)) 
                # Read one byte.
                val = self.ucontr_conn.readline(1)
                print val
                x += 1

            x = 9
            while x>0:
                # Send one byte.
                self.ucontr_conn.write(chr(x)) 
                # Read one byte.
                val = self.ucontr_conn.readline(1)
                print val
                x -= 1


        # Close connection.
        self.ucontr_conn.close()


