import serial
import sys

class UControllerManager:
    ucontrConn = None

    # Create the serial connections we need
    def __init__(self,
                 bps=9600,
                 port='/dev/ttyACM1',
                 timeout=1,
                 parity=serial.PARITY_EVEN,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS):

        self.ucontrConn = serial.Serial()
        self.ucontrConn.baudrate = bps
        self.ucontrConn.port = port
        self.ucontrConn.timeout = timeout
        self.ucontrConn.parity = parity
        self.ucontrConn.stopbits = stopbits
        self.ucontrConn.bytesize = bytesize

        # Try to open the connection.
        self.ucontrConn.open()
        if not self.ucontrConn.isOpen():
            sys.exit("Failed opening serial connection for ucontroller.")

    def __del__(self):
        # Close the connection.
        self.ucontrConn.close()

    # Send command to move forward.
    def forward(self, params):
        val = params['value']
        print "Moving forward by ", val
        self.ucontrConn.write(chr(val))

    # Send command to reverse.
    def reverse(self, params):
        val = params['value']
        print "Reversing by ", val
        self.ucontrConn.write(chr(val))

    # Send command to turn.
    def turn(self, params):
        val = params['value']
        print "Turning by ", val
        self.ucontrConn.write(chr(val))

'''
    def run(self):
        # Start of main loop.
        print "Main loop running."
        while x<10:
            # Read one byte.
            val = self.ucontrConn.readline(1)
            print val
            x += 1
'''

