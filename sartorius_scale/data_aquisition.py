import numpy as np
import serial_ports_find
import mettler_toledo_device
import csv
import time

def update_tss(start_time):
    return time.time() - start_time

scale = serial_ports_find.connect_scale()

if scale == None:
    scale = serial_ports_find.custom_connect_scale()

scale.ser.timeout = .1

print(scale.ser)

file_out = open('data.csv', 'w', newline='')
csv_writer = csv.writer(file_out)
start_time = time.time()
tss = update_tss(start_time)

while(True):
    print(scale.read_screen().decode('utf-8'))
    time.sleep(1)
    tss = update_tss(start_time)
    csv_writer.writerow([tss, scale.read_screen().decode('utf-8')])

