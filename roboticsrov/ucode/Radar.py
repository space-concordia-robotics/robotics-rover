from ArduinoControlRev2 import Arduino
from Servo import Servo
from DataFile import DataFile
import numpy as np
import time

class Radar:

    def __init__(self, PORT='COM3', BAUD_RATE=9600):
        servo_x = Servo("servo_x",slope=11.029, intercept=402.42, lower_limit=20, upper_limit=160)
        servo_y = Servo("servo_y",slope=10.364, intercept=515.79, lower_limit=60, upper_limit=120)
        self.arduino = Arduino(servo_x, servo_y, port=PORT, baud_rate=BAUD_RATE)
        self.x_range = self.arduino.servo_x.get_rotation_range()
        self.y_range = self.arduino.servo_y.get_rotation_range()
        self.com_distance = 'd'
        self.com_rotate_x = 'x'
        self.com_rotate_y = 'y'
        self.com_reset_variables = 'r'
        self.com_center_servos = 'c'
        self.arduino.write_then_read(self.com_center_servos, 1)

    def scan(self):

        start_time = time.time()
        raw_data = np.empty([self.x_range.shape[0]*self.y_range.shape[0], 3], dtype=np.int32)
        raw_data[:,0] = np.tile(self.x_range, self.y_range.shape[0])
        raw_data[:,1] = np.repeat(self.y_range, self.x_range.shape[0])
        raw_data[:,2] = 0

        index = 0

        for y_angle in self.y_range:
            self.arduino.write_then_read(self.com_rotate_y, 1)
            print "Angle: {} -->".format(y_angle)

            for x_angle in self.x_range:
                self.arduino.write_then_read(self.com_rotate_x, 1)
                raw_data[index,2] = self.arduino.write_then_read(self.com_distance, "dynamic")
                # print "Distance {} mm".format(raw_data[index,2])
                index += 1

        print "It took {} seconds for full rotation".format(time.time() - start_time)

        self.arduino.write_then_read(self.com_reset_variables, 1)
        self.arduino.write_then_read(self.com_center_servos, 1)

        self.output_to_csv(raw_data)


    def continuous_readings(self):

        while True:
            print self.arduino.write_then_read('d', "dynamic")

    def output_to_csv(self, data):
        csv_file = DataFile(r"lidar_scan_data\test2.csv")
        csv_file.write_header(["angleX", "angleY", "distance"])
        csv_file.write_array(data)
        csv_file.close_file()



if __name__=="__main__":
    radar = Radar()
    radar.scan()