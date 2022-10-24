from guizero import App, PushButton, Window, ButtonGroup, TextBox, Text
from config import motors_config_list
import csv
import time
import threading
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from config import motors_config_list
import time
import os
from pick import pick
import sys
from SpotClass import Spot
from IKUD import IKUD

chosen_motor = None
    
Spot = Spot()
IKUD = IKUD()
stop_threads = 0

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus, address = 0x42)
pca.frequency = 50

L0 = 5
shoulder_angle = 90

def calibration_process(max_pulse, min_pulse, rotate, chosen_motor):
    active_joint = servo.Servo(pca.channels[motors_config_list[chosen_motor-1]["channel"]])
    active_joint.set_pulse_width_range(min_pulse, max_pulse)
    active_joint.angle = rotate
    time.sleep(0.03)


def open_calibration():
    global chosen_motor
    chosen_motor = motor_button.value
    motor_window.show()

def calibration_screen():
    calibration_window.show()

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
calibration_button = PushButton(app, text="Calibration", command = calibration_screen, align="bottom", height="5", width="fill")

calibration_window = Window(app, title="Calibration Screen", height=320, width=480, visible=False)
motor_window = Window(calibration_window, height=320, width=480, visible=False)
motor_button = ButtonGroup(calibration_window, options = [["rear_shoulder_left", "1"], ["rear_leg_left", "2"], ["rear_feet_left", "3"], ["rear_shoulder_right", "4"], ["rear_leg_right", "5"], ["rear_feet_right", "6"], ["front_shoulder_left", "7"], ["front_leg_left", "8"], ["front_feet_left", "9"], ["front_shoulder_right", "10"], ["front_leg_right", "11"], ["front_feet_right", "12"]], command=open_calibration)
max_pulse_text = Text(motor_window, text="Enter maximum pulse width: ")
max_pulse = TextBox(motor_window, text = "")
min_pulse_text = Text(motor_window, text="Enter minimum pulse width: ")
min_pulse = TextBox(motor_window, text = "")
rotate_text = Text(motor_window, text="Enter angle of rotation: ")
rotate = TextBox(motor_window, text = "")
update_values = PushButton(motor_window, text="Update Data", command = lambda: calibration_process(int(max_pulse.value), int(min_pulse.value), int(rotate.value), int(chosen_motor)))

app.display()

