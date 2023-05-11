import numpy as np
import serial_ports_find
from scaledrivers import scale, mettlertoledo, sartorius
import csv
import time
import data_class
import keyboard

def update_tss(start_time):
    return time.time() - start_time

scale = serial_ports_find.connect_scale()

# Commented out until testing is done
# if scale == None:
#     scale = serial_ports_find.custom_connect_scale()

# TESTING CODE #
scale = mettlertoledo.MettlerToledo('COM5')
# END OF TESTING CODE #

scale.ser.timeout = .1

print(scale.ser)
collector = data_class.DataCollect(scale=scale, unit='g', time_unit='s', delay=1, delay_overall=True)

break_key = 'q'
start_key = 's'
stop_key = 'e'
next_column_key = 'n'
force_measure_key = 'f'
columns = []  # List of columns to print out
columns.append(0)
last_key_pressed = None

while(True):
    if keyboard.is_pressed(break_key):
        scale.sound()
        break
    if keyboard.is_pressed(start_key) and not collector.go_measure:
        scale.sound()
        collector.StartMeasure()
    if keyboard.is_pressed(next_column_key) and last_key_pressed != next_column_key:
        scale.sound()
        collector.NextColumn()
        columns.append(columns[-1] + 1)
        last_key_pressed = next_column_key
    if keyboard.is_pressed(force_measure_key) and last_key_pressed != force_measure_key or True:  # Testing with forced collection
        scale.sound()
        collector.AddMeasure(force = True)
        last_key_pressed = force_measure_key
    if not keyboard.is_pressed(next_column_key or force_measure_key):
        last_key_pressed = None
    if keyboard.is_pressed(stop_key):
        scale.sound()
        collector.StopMeasure()
    collector.AddMeasure()

collector.ExportData('test.csv', columns = columns, times=True)
