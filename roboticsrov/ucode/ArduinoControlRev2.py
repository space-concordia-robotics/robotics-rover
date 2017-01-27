import re
import serial
import sys
import time


class Arduino:

    def __init__(self, servo_x, servo_y, port, baud_rate=9600):
        self.port_name = port
        self.baud_rate = baud_rate
        self.servo_x = servo_x
        self.servo_y = servo_y
        self.arduino = serial.Serial(self.port_name, self.baud_rate, bytesize=serial.EIGHTBITS, timeout=2)
        time.sleep(2)

        attempt = 1
        while not self.arduino_ready() and attempt <= 10:

            if attempt >= 2:
                print "Trying to read ready state from Arduino, attempted {} of {}".format(attempt, 10)
                time.sleep(1)

            if attempt == 10:
                print "Cannot connect to Arduino. Shutting down"
                sys.exit()

            attempt += 1

    def arduino_ready(self):
        ready_command = self.read_command(num_bytes=1)  # Read first command from Arduino

        if ready_command == "r":
            print "Arduino is ready"
            self.status = True
            return True
        elif ready_command is None:
            print "Arduino is not ready"
            self.status = False
            return False
        else:
            print "Check timeout value (increase)"
            self.status = False
            return False

    def read_command(self, num_bytes):
        # Get the number of bytes (first byte sent from Arduino Serial Port)
        # Waits for first byte to be in serial buffer
        if num_bytes == "dynamic":
            # Read first value, which is number of incoming bytes
            while self.arduino.in_waiting == 0:
                # print "Loop1"
                pass

            num_bytes = int(self.arduino.read(1))

        # Checks for command from Arduino
        while self.arduino.in_waiting < num_bytes:
            # print "Loop2"
            pass

        return self.arduino.read(num_bytes)  # read num bytes

    def write_command(self, command):
        """
        :param command: command to be sent to arduino
        :return: returns confirmation message
        """

        self.arduino.write(command)

        # print "Writing... "
        while self.arduino.out_waiting > 0:  # Waits for arduino to process written command
            pass
        # print "Done writing! "


    def write_then_read(self, command, num_bytes):
        self.write_command(command)
        return self.read_command(num_bytes)


    def close_arduino(self):
        self.arduino.close()


if __name__ == "__main__":
    servo_x = Servo("servo_x",slope=11.029, intercept=402.42, lower_limit=20, upper_limit=160)
    servo_y = Servo("servo_y",slope=10.364, intercept=515.79, lower_limit=60, upper_limit=120)
    arduino = Arduino(servo_x, servo_y, 'COM3')

    t_in = 0
    t_out = 0
    while True:
        t_in = time.time()
        print "{} mm took {} ms " .format(int(arduino.get_distance())*10, 1000*(time.time()-t_in))