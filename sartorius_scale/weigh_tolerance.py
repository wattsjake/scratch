from serial.tools.list_ports import comports
import PySimpleGUI as sg
import data_class
from scaledrivers import scale, mettlertoledo, sartorius
from scaledrivers.scale import Scale


# From PySimpleGUI cookbook
def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, pad=(0, 0)))


sg.theme('DarkTeal1')   # Add a touch of color

# Scale selection layout and information

port_list = comports()

scale_selection_layout = [[sg.Push(), sg.Text('Serial Port:'), sg.Combo(port_list, key='-PORT-SELECTION-')],
                          [sg.Push(), sg.Text('Please select the scale manufacturer:'), sg.Combo([*scale.manufacturers], key='-SCALE-SELECTION-', enable_events=True)],
                          [sg.Push(), collapse([[sg.Text('Please select the scale model:'), sg.Combo([], key='-SCALE-MODEL-')]], '-SCALE-MODEL-SECTION-')],
                          [sg.Push(), sg.Button('Continue', key="-CONTINUE-"), sg.Exit(), sg.Push()]]

scale_selection_window = sg.Window('Scale Selection', scale_selection_layout)

scale_selection_window.read(timeout=0)
scale_selection_window['-SCALE-MODEL-SECTION-'].update(visible=False)

while True:
    event, values = scale_selection_window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-SCALE-SELECTION-':
        scale_selection_window['-SCALE-MODEL-'].update(values=[*(scale.manufacturers[values['-SCALE-SELECTION-']].scales)])
        scale_selection_window['-SCALE-MODEL-SECTION-'].update(visible=True)
    if event == '-CONTINUE-':
        if values['-SCALE-SELECTION-'] in scale.manufacturers.keys():
            manufacturer = scale.manufacturers[values['-SCALE-SELECTION-']]
            if values['-SCALE-MODEL-'] in manufacturer.scales.keys():
                scale1 = scale.manufacturer_scales[manufacturer][values['-SCALE-MODEL-']](values['-PORT-SELECTION-'].device)
            else:
                scale1 = manufacturer(values['-PORT-SELECTION-'].device)
        else:
            scale1 = Scale(values['-PORT-SELECTION-'])
        scale_selection_window.close()
        break

# create a window with a weight reading and a horizontal rectangle below it, and a vertical rectangle inside of the horizontal rectangle
# the vertical rectangle will be green if the weight is within tolerance, and red if it is not
# the horizontal rectangle will be green if the weight is within tolerance, and red if it is not

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