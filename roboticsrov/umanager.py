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
        self.port = port
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.uConn = None

        
        # Try to connect to port. If no connection is found, verify that the user is in the 'dialout' group - this enables access to serial out.
        portList = self.serial_ports()
        print portList

        if portList == None:
            sys.exit("No ports found.") 
        else:
            port_selected = int(raw_input("Which port do you want to connect to for the microcontroller? (starting from index0)"))
            self.port = portList[port_selected]

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
        if direction == 'forward' or direction == "reverse" or direction == "forwardLeft" or direction == "forwardRight"or direction == "reverseLeft" or direction == "reverseRight":
            return True if val in range(1, 64) else False

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
            self.sendCommand(64 - value)
            self.sendCommand(value + 192)

    def reverse(self, params):
        """ Send command to reverse. """
        value = params['value']

        if self.validateVal('reverse', value):
            print "Reversing by ", value
            self.sendCommand(value + 64)
            self.sendCommand((64 - value) + 128)

    def forwardLeft(self, params):
        """ Send command to turn left. """
        value = params['value']

        if self.validateVal('forwardLeft', value):
            value = value * 21 / 64 # value should only go up to 21
            print "Turning left with value ", value
            self.sendCommand(22 - value)
            self.sendCommand(192 + value)

    def forwardRight(self, params):
        """ Send command to turn right."""
        value = params['value']

        if self.validateVal('forwardRight', value):
            value = value * 21 / 64 
            print "Turning right with value " , value
            self.sendCommand(64 - value)
            self.sendCommand(233 + value)

    def reverseLeft(self, params):
        """ Send command to reverse left."""
        value = params['value']
        if self.validateVal('reverseLeft', value):
            value = value * 21 / 64
            print "Reversing left with value ",value
            self.sendCommand(107+value)
            self.sendCommand(192-value)

    def reverseRight(self, params):
        """ Send command to reverse right."""
        value = params['value']
        if self.validateVal('reverseRight', value):
            value = value * 21 / 64 
            print "Reversing right with value ",value
            self.sendCommand(64+value)
            self.sendCommand(150-value)

    def stop(self, params):
        """ Send command to stop motors."""
        print "Stopping motors."
        self.sendCommand(0)
