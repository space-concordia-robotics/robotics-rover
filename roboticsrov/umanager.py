import serial
import sys
import glob
import time

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
         #   self.port = port
        self.port = '/dev/ttyACM1'
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.uConn = None

        
        # Try to connect to port.
        """     portList = self.serial_ports()
        
        if portList == None:
            sys.exit("No ports found.") 
        else:
            self.port = portList[0]
        """

        try:
            self.uConn = serial.Serial(
                                self.port,
                                self.baudrate,
                                self.bytesize,
                                self.parity,
                                self.stopbits,
                                self.timeout)
            self.connected = True
            print "Connected to port.", self.port
        except:
            self.connected = False
            sys.exit("Failed connecting to port.")

        print "Waiting some time for microcontroller's serial to startup..."
        time.sleep(5)	# 5 seconds

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
    
    def validateVal(self, direction, val):
        """ Validates the value before being sent to 
            the microcontroller.

            Returns: true when value is within range else false
        """
        if direction == 'forward':
            return True if val in range(65, 128) or val in range(193, 256) else False

        elif direction == 'reverse':
            return True if val in range(1, 64) or val in range(128, 192) else False

        elif direction == 'turnLeft' or direction == 'turnRight':
            return True if val in range(0, 256) else False

        elif direction == 'stop':
            return True if val==0 or val==64 or val==192 else False

        else:
            print "Wtf. What are you doing here? Value out of range."
            return False

    def sendCommand(self, value):
        numBytesSent = self.uConn.write(chr(value))
        print "chr value: ", chr(value)
        print "Number of bytes sent: ", numBytesSent

    def forward(self, params):
        """ Send command to move forward. """
        value = params['value']

        if self.validateVal('forward', value):
            print "Moving forward by ", value
            self.sendCommand(value)

#            v = self.uConn.read()
#            print v
#            print ord(v)

    def reverse(self, params):
        """ Send command to reverse. """
        value = params['value']

        if self.validateVal('reverse', value):
            print "Reversing by ", value
            self.sendCommand(value)

    def turnLeft(self, params):
        """ Send command to turn left. """
        value = params['value']

        if self.validateVal('turnLeft', value):
            print "Turning left with value ", value
            self.sendCommand(value)

    def turnRight(self, params):
        """ Send command to turn right."""
        value = params['value']

        if self.validateVal('turnRight', value):
            print "Turning right with value " , value
            self.sendCommand(value)

    def stop(self, params):
        """ Send command to stop motors."""
        value = params['value']
        
        if self.validateVal('stop', value):
            print "Stopping motor with value", value
            self.sendCommand(value)
