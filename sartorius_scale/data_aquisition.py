import numpy as np
import serial_ports_find
import mettler_toledo_device
import csv
import time
import data_class
import keyboard

def update_tss(start_time):
    return time.time() - start_time

scale = serial_ports_find.connect_scale()

if scale == None:
    scale = serial_ports_find.custom_connect_scale()

scale.ser.timeout = .1

print(scale.ser)
collector = data_class.DataCollect(scale=scale, unit='g', time_unit='s', delay=0.5, delay_overall=True)

break_key = 'q'
start_key = 's'
stop_key = 'e'

while(True):
    data = scale.read_screen().decode('utf-8')
    print(data)
    data = data.split(' ')
    if keyboard.is_pressed(break_key):
        break
    if keyboard.is_pressed(start_key) and not collector.go_measure:
        collector.StartMeasure(data[5])
    if keyboard.is_pressed(stop_key):
        collector.StopMeasure()
    collector.AddMeasure(data[5])

collector.ExportData('test.csv')
