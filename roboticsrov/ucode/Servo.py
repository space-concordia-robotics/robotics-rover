import numpy as np

class Servo:

    def __init__(self, servo_name, slope, intercept, lower_limit, upper_limit):
        """
        constructor
        :param servo_name: either servo_x or servo_y
        :param slope: microsecond/degree
        :param intercept: microsecond
        :param lower_limit: lower angle limit
        :param upper_limit: upper angle limit
        """
        self.servo_name = servo_name
        self.current_angle = 0
        self.slope = slope  #microseconds/degree
        self.intercept = intercept  #microseconds
        self.lower_limit = lower_limit  #lower angle limit
        self.upper_limit = upper_limit  #upper angle limit
        self.lower_pwm = self.get_pwm_from_angle(lower_limit)
        self.upper_pwm = self.get_pwm_from_angle(upper_limit)

    def get_current_angle(self):
        """
        :return: current angle servo is pointing at
        """
        return self.current_angle

    def set_current_angle(self, current_angle):
        """
        Sets current angle of servo
        :param current_angle: current angle to set
        :return:
        """
        self.current_angle = current_angle
        # print "Current angle set to {} for {}".format(self.current_angle, self.servo_name)

    def get_pwm_from_angle(self, angle):
        """
        calculates pwm in microseconds from angle in order to rotate servo
        :param angle: angle to rotate to, in degrees
        :return:
        """
        if (angle < self.lower_limit or angle > self.upper_limit):
            print "Angle {} not between [{},{}]".format(angle, self.lower_limit, self.upper_limit)
            return None

        pwm = int(self.slope*angle + self.intercept)
        return pwm

    def get_rotation_range(self):
        """
        creates a range of angles that increment by 1
        [lower_limit, upper_limit]
        :return: (see above)
        """
        return np.arange(start=self.lower_limit, stop=self.upper_limit+1)

    def __str__(self):
        strRep = ""
        for key in self.__dict__:
            strRep += "{}: {}\n".format(key, self.__dict__[key])

        return strRep

