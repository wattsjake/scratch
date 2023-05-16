import PySimpleGUI as sg
import data_class
from scaledrivers import scale, mettlertoledo, sartorius

# create a window with a weight reading and a horizontal rectangle below it, and a vertical rectangle inside of the horizontal rectangle
# the vertical rectangle will be green if the weight is within tolerance, and red if it is not
# the horizontal rectangle will be green if the weight is within tolerance, and red if it is not

sg.theme('DarkTeal1')

layout = [[sg.Text(key='-CURRENT-MEASURE-'), sg.Text(key='-CURRENT-UNIT-')],
          [sg.Text(key='-INSTRUCTION-')],
        #   [sg.], Will be used for bar showing tolerance
          [sg.Push(), sg.Text('Please enter the target measurement: '), sg.Input(key='-TARGET-')],
          [sg.Push(), sg.Text('Please enter the unit (defaults to measurement unit): '), sg.Input(key='-UNIT-')],
          [sg.Push(), sg.Text('Please select the type of tolerance: '), sg.Radio('Percent (%)', "TOLERANCE-TYPE", default=True, key="-TOLERANCE-IS-PERCENT-"),
               sg.Radio('Amount (Unit)', "TOLERANCE-TYPE", default=False), sg.Push()],
          [sg.Push(), sg.Text('Please enter the tolerance: '), sg.Input(key='-TOLERANCE-')],
          [sg.Button('Continue'), sg.Exit()]]

window = sg.Window('Chemistry Lab', layout)

# Stages:
# 1. Get the scale that will be used
# 2. Get the target measurement, unit, and tolerance
# 3. Measure with scale until a stable measurement within tolerance is reached
stage = 1
stage_started = False

while True:                             # The Event Loop
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if stage == 1:
        if not stage_started:
            window['-INSTRUCTION-'].update('Please place the object to be measured on the scale and press continue.')
            stage_started = True


window.close()