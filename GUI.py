
from guizero import App, Text, PushButton
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
import threading
from adafruit_motor import servo
from config import motors_config_list
import csv
import time
from SpotClass import Spot
from IKUD import IKUD

Spot = Spot()
IKUD = IKUD()
stop_threads = 0

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus, address = 0x42)
pca.frequency = 50

L0 = 5
shoulder_angle = 90

def rest_position():
    global L0
    L0 = 5
    joint_counter = 0
    while joint_counter < 12:
        joint = servo.Servo(pca.channels[motors_config_list[joint_counter]["channel"]])
        joint.set_pulse_width_range(motors_config_list[joint_counter]["min_pulse"],motors_config_list[joint_counter]["max_pulse"])
        joint.angle = int(motors_config_list[joint_counter]["rest_angle"])
        joint_counter += 1

def move_up():
    global L0
    shoulder_angle = 90
    L0 += 1
    print(L0)
    leg_angle, feet_angle = IKUD.calculate_angle(L0)
    Spot.turn_motor(shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle, shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle)
    print(shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle, shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle)

def move_down():
    global L0
    shoulder_angle = 90
    L0 -= 1
    leg_angle, feet_angle = IKUD.calculate_angle(L0)
    Spot.turn_motor(shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle, shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle)
    print(shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle, shoulder_angle, leg_angle, feet_angle, 180-shoulder_angle, 180-leg_angle, 180-feet_angle)

def walk():
    while True:
        global stop_threads
        with open('Walk_Angles.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # print(float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]))
                    Spot.turn_motor(float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]))
                    time.sleep(0.008)
                    if (stop_threads%2 == 0):
                        return

def walk_queue():
    global stop_threads
    stop_threads += 1
    p = threading.Thread(target = walk)
    if (stop_threads%2 == 1):
        p.start()
        print("Start")
    else:
        print("Terminate")

app = App("MAIN", height=320, width=480)

down_button = PushButton(app, text="Down", command = move_down, align="bottom", height="fill", width="fill")
up_button = PushButton(app, text="Up", command = move_up, align="bottom", height="fill", width="fill")
walk_button = PushButton(app, text="Walk", command=walk_queue, align="right", height="5", width="fill")
rest_button = PushButton(app, text="Rest", command = rest_position, align="left", height="5", width="fill")

app.display()