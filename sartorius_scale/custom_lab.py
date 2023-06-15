from serial.tools.list_ports import comports
import PySimpleGUI as sg
from scaledrivers import scale, mettlertoledo, sartorius
import fastnumbers as fn

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

