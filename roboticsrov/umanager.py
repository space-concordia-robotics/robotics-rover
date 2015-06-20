import serial
import sys
import glob

class UManager:

    # Create the serial connections we need.
    def __init__(self,
                 bps=9600,
                 port=None,
                 timeout=1,
                 parity=serial.PARITY_EVEN,
                 stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS):

        self.baudrate = bps
        self.port = port
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.uConn = None

        # Try to connect to port.
        portList = self.serial_ports()

        if portList == None:
            sys.exit("No ports found.") 
        else:
            self.port = portList[0]

        try:
            self.uConn = serial.Serial(
                                self.port,
                                self.baudrate,
                                self.bytesize,
                                self.parity,
                                self.stopbits,
                                self.timeout)
            print "Connected to port.", self.port
        except:
            self.connected = False
            sys.exit("Failed connecting to port.")

    def __del__(self):
        # Close the connection.
        if self.connected and self.uConn.isOpen():
            self.uConn.close()


    def serial_ports(self):
        """Lists serial ports
                
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = [] 
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result
    
    def forward(self, params):
        """ Send command to move forward. """
        val = params['value']
        print "Moving forward by ", val
        self.ucontrConn.write(chr(val))

    def reverse(self, params):
        """ Send command to reverse. """
        val = params['value']
        print "Reversing by ", val
        self.ucontrConn.write(chr(val))

    def turn(self, params):
        """ Send command to turn. """
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

