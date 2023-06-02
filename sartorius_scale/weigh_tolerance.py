from serial.tools.list_ports import comports
import PySimpleGUI as sg
import data_class
from scaledrivers import scale, mettlertoledo, sartorius
from scaledrivers.scale import Scale
import fastnumbers as fn


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

def string_to_measure(measure: str):
    measure = measure.replace(" ", "")

    data = data_class.Data()

    for i in range(len(measure)):
        if not measure[len(measure)-i-1].isalpha():
            data.unit = measure[len(measure)-i:]
            data.value = fn.try_float(measure[:len(measure)-i], on_fail=fn.RAISE)
            return data


class MultiLayoutWindow(sg.Window):

    def __init__(self, layouts, **kwargs):

        final_layout = []

        for layout in layouts:
            final_layout.append(sg.Column(layout=layout, visible=False, key=self.get_layout_key(layouts.index(layout))))
        super().__init__(layout=[final_layout], **kwargs)
        self.current_layout = kwargs.get("start_layout", 0)
        self.max_layout = len(layouts)

    def change_layout(self, layout_number):
        if 0 <= layout_number < self.max_layout:
            if self.current_layout != layout_number:
                self[self.get_layout_key(self.current_layout)].update(visible=False)
                self.current_layout = layout_number
            self[self.get_layout_key(self.current_layout)].update(visible=True)
            return True
        else:
            return False

    def next_layout(self):
        return self.change_layout(self.current_layout + 1)

    def previous_layout(self):
        return self.change_layout(self.current_layout - 1)

    def get_layout(self):
        return self.current_layout

    def get_layout_key(self, layout):
        return "-COL" + "-" + str(layout) + "-"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)



sg.theme('DarkTeal1')   # Add a touch of color

# Scale selection layout and information

port_list = comports()

scale_selection_layout = [[sg.Push(), sg.Text('Serial Port:'), sg.Combo(port_list, key='-PORT-SELECTION-')],
                          [sg.Push(), sg.Text('Scale Manufacturer:'), sg.Combo([*scale.manufacturers], key='-SCALE-SELECTION-', enable_events=True)],
                          [sg.Push(), collapse([[sg.Text('Scale Model:'), sg.Combo([], key='-SCALE-MODEL-')]], '-SCALE-MODEL-SECTION-')],
                          [sg.Push(), sg.Button('Continue', key="-CONTINUE-0-"), sg.Exit(), sg.Push()]]

tolerance_input_layout = [[sg.Push(), sg.Text('Target measurement (include unit): '), sg.Input(key='-TARGET-', enable_events=True)],
                          [sg.Push(), sg.Text('Type of tolerance: '), sg.Radio('Percent (%)', "TOLERANCE-TYPE", default=True, key="-TOLERANCE-IS-PERCENT-"),
                             sg.Radio('Amount (Unit)', "TOLERANCE-TYPE", default=False), sg.Push()],
                          [sg.Push(), sg.Text('Please enter the tolerance: '), sg.Input(key='-TOLERANCE-', enable_events=True)],
                          [sg.Button('Continue', key="-CONTINUE-1-"), sg.Exit()]]

tolerance_measure_layout = [[sg.Push(), sg.Text('Please tare the scale to begin.', key='-INSTRUCTION-2-')]]

window = MultiLayoutWindow([scale_selection_layout, tolerance_input_layout, tolerance_measure_layout], title='Chemistry Lab')

# tolerance_measure_layout = [[sg.Push(), sg.Text('Please place the item on the scale and press the button below to measure it.'), sg.Push()],
                            

# window = sg.Window('Scale Selection', scale_selection_layout)

window.read(timeout=0)
window.change_layout(0)
window['-SCALE-MODEL-SECTION-'].update(visible=False)

prev_target = ""

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # Scale selection events
    if window.get_layout() == 0:
        if event == '-SCALE-SELECTION-':
            window['-SCALE-MODEL-'].update(values=[*(scale.manufacturers[values['-SCALE-SELECTION-']].scales)])
            window['-SCALE-MODEL-SECTION-'].update(visible=True)
        if event == '-CONTINUE-0-':
            if values['-SCALE-SELECTION-'] in scale.manufacturers.keys():
                manufacturer = scale.manufacturers[values['-SCALE-SELECTION-']]
                if values['-SCALE-MODEL-'] in manufacturer.scales.keys():
                    scale1 = scale.manufacturer_scales[manufacturer][values['-SCALE-MODEL-']](values['-PORT-SELECTION-'].device)
                else:
                    scale1 = manufacturer(values['-PORT-SELECTION-'].device)
            else:
                scale1 = Scale(values['-PORT-SELECTION-'])
            window.next_layout()

    # Tolerance input events
    if window.get_layout() == 1:
        if event == '-TARGET-':
            try:
                target_measure = string_to_measure(values['-TARGET-'])
                prev_target = values['-TARGET-']
            except ValueError:
                window['-TARGET-'].update(value=prev_target)
        if event == '-CONTINUE-1-':
            if target_measure.measure == None or target_measure.unit == "":
                sg.popup_error("Please enter a valid target measurement.")
            else:
                if values['-TOLERANCE-IS-PERCENT-']:
                    tolerance = (fn.try_float(values['-TOLERANCE-']) / 100) * target_measure.measure
                else:
                    tolerance = fn.try_float(values['-TOLERANCE-'])
                window.next_layout()

            

    # Tolerance measure events


# Columns:
# 0. Get the scale that will be used
# 1. Get the target measurement, unit, and tolerance
# 2. Measure with scale until a stable measurement within tolerance is reached



window.close()