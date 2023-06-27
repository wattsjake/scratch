from serial.tools.list_ports import comports
import PySimpleGUI as sg
from scaledrivers import scale
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


class MultiLayoutWindow(sg.Window):

    def __init__(self, layouts, **kwargs):

        final_layout = []
        self.layout_keys = list(layouts.keys())

        for layout_key in self.layout_keys:
            final_layout.append(sg.Column(
                layout=layouts[layout_key], 
                visible=(layout_key == kwargs.get("start_layout", self.layout_keys[0])), 
                key=layout_key
            ))
        self.current_layout = kwargs.get("start_layout", self.layout_keys[0])
        kwargs.pop("start_layout", None)
        super().__init__(layout=[final_layout], **kwargs)

    def change_layout(self, layout_key):
        if layout_key in self.layout_keys:
            if layout_key != self.current_layout:
                self[self.current_layout].update(visible=False)
                self[layout_key].update(visible=True)
                self.current_layout = layout_key
        else:
            raise KeyError("Layout key not found")

    def get_layout(self):
        return self.current_layout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)



sg.theme('DarkTeal1')   # Add a touch of color

# Scale selection layout and information

port_list = comports()

scale_selection_layout = [[sg.Push(), sg.Text('Serial Port:'), sg.Combo(port_list, key='-PORT-SELECTION-')],
                          [sg.Push(), sg.Text('Scale Manufacturer:'), sg.Combo([*scale.manufacturer_scales], key='-SCALE-SELECTION-', enable_events=True)],
                          [sg.Push(), collapse([[sg.Text('Scale Model:'), sg.Combo([], key='-SCALE-MODEL-')]], '-SCALE-MODEL-SECTION-')],
                          [sg.Push(), sg.Button('Continue', key="-CONTINUE-0-"), sg.Exit(), sg.Push()]]

tolerance_input_layout = [[sg.Push(), sg.Text('Target measurement (include unit): '), sg.Input(key='-TARGET-', enable_events=True)],
                          [sg.Push(), sg.Text('Type of tolerance: '), sg.Radio('Percent (%)', "TOLERANCE-TYPE", default=True, key="-TOLERANCE-IS-PERCENT-"),
                             sg.Radio('Amount (Unit)', "TOLERANCE-TYPE", default=False), sg.Push()],
                          [sg.Push(), sg.Text('Please enter the tolerance: '), sg.Input(key='-TOLERANCE-', enable_events=True)],
                          [sg.Push(), sg.Button('Continue', key="-CONTINUE-1-"), sg.Exit(), sg.Push()]]

tolerance_measure_layout = [[sg.Push(), sg.Text('Add weight to begin measuring.', key='-INSTRUCTION-2-'), sg.Push()],
                            [sg.Push(), sg.Button('Tare', key='-TARE-'), sg.Exit(), sg.Push()]]

instruction_layout = [[sg.Push(), sg.Text('Connecting to scale...', key='-INSTRUCTION-1-'), sg.Push()],
                      [sg.Push(), sg.Exit(), sg.Push()]]

window = MultiLayoutWindow(
    {
        "scale_selection": scale_selection_layout, 
        "tolerance_input": tolerance_input_layout, 
        "tolerance_measure": tolerance_measure_layout, 
        "instruction": instruction_layout
    },
    start_layout="instruction",
    title='Chemistry Lab'
)

window.read(timeout=0)

scale1 = scale.auto_connect_scale()
if scale1 is None:
    window.change_layout("scale_selection")
    window['-SCALE-MODEL-SECTION-'].update(visible=False)
else:
    scale1.send_receive("D \"Lab\"")
    window.change_layout("tolerance_input")

prev_target = ""

while True:
    event, values = window.read(timeout=100)
    # print(event, values)
    if event == sg.WIN_CLOSED:
        break
    if isinstance(event, str):
        if 'Exit' in event:
            break

    # Scale selection events
    if window.get_layout() == "scale_selection":
        if event == '-SCALE-SELECTION-':
            window['-SCALE-MODEL-'].update(values=scale.manufacturer_scales[values['-SCALE-SELECTION-']])
            window['-SCALE-MODEL-SECTION-'].update(visible=True)
        if event == '-CONTINUE-0-':
            if values['-SCALE-SELECTION-'] in scale.manufacturer_scales.keys():
                manufacturer = values['-SCALE-SELECTION-']
                if values['-SCALE-MODEL-'] in scale.manufacturer_scales[manufacturer]:
                    scale1 = values['-SCALE-MODEL-'](values['-PORT-SELECTION-'].device)
                else:
                    scale1 = manufacturer(values['-PORT-SELECTION-'].device)
            else:
                scale1 = scale.Scale(values['-PORT-SELECTION-'])
            scale1.send_receive("D \"Lab\"")
            window.change_layout("tolerance_input")

    # Tolerance input events
    if window.get_layout() == "tolerance_input":
        if event == '-TARGET-':
            try:
                target_measure = scale.string_to_measure(values['-TARGET-'])
                prev_target = values['-TARGET-']
            except ValueError:
                window['-TARGET-'].update(value=prev_target)
        if event == '-CONTINUE-1-':
            if target_measure.measure == None or target_measure.unit == "":
                sg.popup_error("Please enter a valid target measurement.")
            else:
                if values['-TOLERANCE-IS-PERCENT-']:
                    tolerance = fn.try_float(values['-TOLERANCE-']) / 100
                else:
                    tolerance = fn.try_float(values['-TOLERANCE-']) / target_measure.measure
                window.change_layout("tolerance_measure")

    # Tolerance measure events
    if window.get_layout() == "tolerance_measure":
        try:
            measurement = scale1.get_weight_data()

            if measurement.stable:
                if abs(measurement.measure - target_measure.measure) <= tolerance * target_measure.measure:
                    window['-INSTRUCTION-2-'].update("Measurement is within tolerance. Please remove the item from the scale.")
                else:
                    amount_text = ""
                    if abs(measurement.measure - target_measure.measure) <= tolerance * 1.5 * target_measure.measure:
                        amount_text = "a little "
                    direction_text = "Add "
                    if measurement > target_measure:
                        direction_text = "Remove "
                    window['-INSTRUCTION-2-'].update("Measurement not within tolerance. " + direction_text + amount_text + "more.")
            else:
                window['-INSTRUCTION-2-'].update("Measurement in progress. Please wait.")
        except scale.ScaleMeasurementException as e:
            window['-INSTRUCTION-2-'].update(e)

        if event == '-TARE-':
            scale1.tare()
        


# Columns:
# 0. Get the scale that will be used
# 1. Get the target measurement, unit, and tolerance
# 2. Measure with scale until a stable measurement within tolerance is reached


scale1.send_receive("DW")
window.close()