import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class PointCloud:

    def __init__(self):
        self.initial_scan=0  # Will contain [anglex, angley, distance]
        self.point_cloud_1=0  # Will contain [x,y,z] coordinates
        self.point_cloud_2=0  # Will contain interpolated [x,y,z] coordinates

    def set_initial_scan(self, raw_data):
        self.initial_scan = raw_data
        self.point_cloud_1 = PointCloud.calculate_point_cloud_1(self.initial_scan)

    @staticmethod
    def calculate_point_cloud_1(raw_data):
        raw_data[:,0] = raw_data[:,0] - 90
        raw_data[:,1] = raw_data[:,1] - 90

        trig = np.zeros((raw_data.shape[0], 4))
        trig[:,0] =np.cos(np.multiply(raw_data[:,0], np.pi/180.0))
        trig[:,1] =np.sin(np.multiply(raw_data[:,0], np.pi/180.0))
        trig[:,2] =np.cos(np.multiply(raw_data[:,1], np.pi/180.0))
        trig[:,3] =np.sin(np.multiply(raw_data[:,1], np.pi/180.0))

        raw_data[:,0] = np.multiply(np.multiply(raw_data[:,2], trig[:,2]), trig[:,1])
        raw_data[:,1] = np.multiply(np.multiply(raw_data[:,2], trig[:,2]), trig[:,0])
        raw_data[:,2] = np.multiply(raw_data[:,2], trig[:,3])

        return raw_data

d = pd.read_csv(r"C:\Users\Anthony Andreoli\Desktop\robotics\robotics_lidar\rev1\python_lidar_servo_control\lidar_scan_data\test2.csv")
raw_data = np.zeros((d.shape[0], d.shape[1]))
raw_data[:,0] = d.angleX.values
raw_data[:,1] = d.angleY.values
raw_data[:,2] = d.distance.values

p = PointCloud()
p.set_initial_scan(raw_data)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.scatter(p.point_cloud_1[:,0], p.point_cloud_1[:,1], p.point_cloud_1[:,2], c='g')
ax.plot_trisurf(p.point_cloud_1[:,0], p.point_cloud_1[:,1], p.point_cloud_1[:,2],antialiased=True)
plt.show()

