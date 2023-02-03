import csv
import PySimpleGUI as sg
import numpy as np
import os.path
from datetime import datetime
import serial 

# Original code for serial communication on sartorious scale

NAME_SIZE=23
data = []
settings = sg.UserSettings(path='.')

tare = b'\x1BU'
print_screen = b'\x1BP'
zero = b'\x1Bf3_'
sound = b'\x1BQ'

def serial_send(parameter):
    try:
        ser.write(parameter)
        print("Serial Send %s" %parameter)
    except NameError as e:
        print('[Error]Connect to scale')


def name(name):
    return sg.Text(name, justification='l',pad=(0,0), font='Consolas 11')

def connect():
    try:
        ser = serial.Serial(
            port='COM4',\
            baudrate=115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
                timeout=0)
    
        print("connected to: " + ser.portstr)
    
    except serial.serialutil.SerialException:
        print("The port is in use. Unplug USB-C")
        
    return ser

def user_settings():
    
    layout = [[sg.Text('User Settings')],
              [sg.T("Save .csv file location"),sg.In(settings.get('-file location-'), k='INPUT',readonly=True),sg.FolderBrowse()],
              #[sg.Checkbox('Auto Increment UTI', default=(settings.get('-inc state-')), key='INC')],
              [sg.Button('Save'),sg.Button('Cancel')]]
    
    window = sg.Window('User Settings', layout, finalize=True, keep_on_top=True)
    
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            print('[LOG]Settings Exit')
            break
        elif event == "Open Folder":
            print('[LOG]Open Folder Clicked')
            
            
        elif event == "Save":
            print('[LOG]Save Clicked')
            print('[LOG]Save .csv file location: ', values['INPUT'])
            settings['-file location-'] = values['INPUT']
            window.close()
            sg.popup(f"Save Location Changed: {values['INPUT']}")
    window.close()
    
        

#---------APPLICATION---------#
sg.theme('SystemDefault1')   # Add a touch of color

title_bar = [sg.T('Sartorius Scale', font='Consolas 13', justification='c', expand_x=True)]

menu_bar = [[sg.Menu([['File', ['Settings','Exit']], ['Help', ['About']]])]]


layout_top = [[sg.Button('Connect')],
              [name('Target Weight:\t'), sg.Input(s=15,k='-Weight-')],
              [sg.Button('Print'),sg.Button('Zero'),sg.Button('Tare'),sg.Button('Sound')]]
    
logging_layout = [[sg.Text("Console Output")],
                  [sg.Multiline(size=(55,12), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                   reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]]

layout = [menu_bar,title_bar,layout_top,logging_layout]





# Create the Window
window = sg.Window('Sartorius Scale Program Rev 0.1', layout)
# Event Loop to process "events" and get the "values" of the inputs 
while True:
    
    
    event, values = window.Read()
    
        
    
    if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('================= Event = ', event, ' ===================')
        print('Event time: ',current_time)
        # print('-------- Values Dictionary (key=value) --------')
        # for key in values:
        #     print(key, ' = ',values[key])
    if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Exit': # if user closes window or clicks cancel
        ser.close()    
        window.close()
        break    
    
    elif event == '-INC-':
        print('[LOG]Auto Increment Clicked')
        #window['-UTI-'].update(disabled=True)
        #window['-UTI-'].update(readonly=False)
        sg.popup('[ERROR] This feature is not available with Unique Creator Rev 1.1,1.2')
        
    #enter settings
    elif event == 'Settings':
        print('[LOG]Settings Clicked')
        user_settings()
        
    elif event == 'About':
        print('[LOG]About Clicked')
        sg.popup('About Sartorius',
                 'This software was created for Dr. Walker of Weber State University',
                 'Copyright 2022 Jacob Watts. All Rights Reserved', keep_on_top=True)
        
    elif event == 'Connect':
        print('[LOG]Connect')
        try:
            ser = connect()
        except:
            print('[Error]No Device Detected')
        
    elif event == 'Print':
        print('[LOG]Print') 
        serial_send(print_screen)
        
    elif event == 'Zero':
        print('[LOG]Zero Clicked')
        serial_send(zero)
    
    elif event == 'Tare':
        print("[LOG]Tare")
        serial_send(tare)
        
    elif event == 'Sound':
        print("[LOG]Sound")
        serial_send(sound)
        
    
        

window.close()
    
