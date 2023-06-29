import serial
from serial.tools.list_ports import comports
import fastnumbers as fn

# Copied over from StackOverflow; author is Jonathan Eunice
def custom_class_repr(name: str, *base_classes: type) -> type:
    """Factory that returns custom metaclass with a class ``__repr__`` that
    returns ``name``.

    :param name: Name to give class object
    :type name: str
    :param \*base_classes: Base classes of the affected class object.
        The metaclasses of these classes are used to make sure the metaclass
        returned by this function is compatible with the metaclasses of the
        base classes.
    :type \*base_classes: type
    :return: Metaclass with custom ``__repr__`` method
    :rtype: type
    """    

    if not base_classes:
        bases = (type,)
    else:
        bases = []
        for base in base_classes:
            bases.append(type(base))
        bases = tuple(bases)

    return type('MetaScale', bases, {'__str__': lambda self: name})

class Scale:
    """Superclass for all scales.

    Stores a collection of methods and attributes that are common to all scales.
    """

    timeout = 2

    def __init__(self, port: str, **kwargs):
        """Initializes a Scale object.

        :param port: Name of port to connect to.
        :type port: str
        """
        
        if not hasattr(self, "DEFAULT_SERIAL"):
            self.DEFAULT_SERIAL = {}
        self.set_serial(port, **kwargs, timeout=self.timeout)
        self.encoding = kwargs.get('encoding', 'utf-8')  # Encoding for serial communication

    # # # SETTERS # # #
    # Used for making a generic scale class in the future.

    def set_baudrates(self, baudrates):
        self.BAUDRATES = baudrates

    def set_bytesizes(self, bytesizes):
        self.BYTESIZES = bytesizes

    def set_stopbits(self, stopbits):
        self.STOPBITS = stopbits

    def set_parities(self, parities):
        self.PARITIES = parities

    def set_tare(self, tare):
        self.TARE = tare

    def set_print_screen(self, print_screen):
        self.PRINT_SCREEN = print_screen

    def set_zero(self, zero):
        self.ZERO = zero

    def set_sound(self, sound):
        self.SOUND = sound

    def set_serial(self, port_: str, **kwargs) -> serial.Serial:
        r"""Sets the serial port for the scale.

        If passed with only a port, the scale will use the default settings for the given scale.
        If the scale has no default settings, it will use the default settings for the serial module.

        Args:
            port_ (str): Name of port to connect to.
            **baudrate (int, optional): Baudrate for serial connection.
            **bytesize (int, optional): Bytesize for serial connection.
            **stopbits (int, optional): Stopbits for serial connection.
            **parity (int, optional): Parity for serial connection.

        Returns:
            serial.Serial: Serial connection made by scale.
        """

        self.ser = serial.Serial(port=port_, **(self.DEFAULT_SERIAL | kwargs))
        
        return self.ser


    # # # METHODS # # #

    def send_receive(self, command: str) -> str:
        r"""Send a command and receive the scale's response.

        Commands are automatically encoded and responses are automatically decoded.
        Check the scale's documentation for a list of commands.

        Args:
            command (str): Command to send to the scale.

        Returns:
            str: The scale's response to the command.
        """

        self.ser.reset_output_buffer()
        self.ser.read_all()
        
        self.ser.write((self.COMMAND_START + command + self.COMMAND_END).encode(self.encoding))
        next_line = self.ser.readline().decode(self.encoding)
        response = next_line
        while not (self.response_complete(next_line) or next_line == ""):
            next_line = self.ser.readline().decode(self.encoding)
            response += next_line

        # If the scale is doing a long command, it might not finish within the timeout, returning a blank line
        # If this happens, the command should be cancelled so it doesn't mess up the next command
        # This feature is not implemented yet

        # if next_line == "":
        #     self.ser.write((self.COMMAND_START + self.CANCEL + self.COMMAND_END).encode(self.encoding))
        #     response += self.ser.readline().decode(self.encoding)

        return response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ser.close()

    def read_screen(self):
        return self.send_receive(self.PRINT_SCREEN)

    def zero(self):
        return self.send_receive(self.ZERO)

    def tare(self):
        return self.send_receive(self.TARE)

    def sound(self):
        return self.send_receive(self.SOUND)
    

from scaledrivers import mettlertoledo, sartorius
import data_class

# Dictionary of all scales by manufacturer
manufacturer_scales = {sartorius.Sartorius: sartorius.scales,
                       mettlertoledo.MettlerToledo: mettlertoledo.scales}

def string_to_measure(measure: str) -> data_class.Data:
    r"""Converts a string to a Data object.

    Args:
        measure (str): Measurement in string form. Must be in the form of a number followed by a unit.
            All spaces will be removed before parsing.

    Returns:
        data_class.Data: Measure with the given value and unit.
    """    
    measure = measure.replace(" ", "")

    data = data_class.Data()

    for i in range(len(measure)):
        if not measure[len(measure)-i-1].isalpha():
            data.unit = measure[len(measure)-i:]
            data.measure = fn.try_float(measure[:len(measure)-i], on_fail=fn.RAISE)
            return data

def auto_connect_scale():
    for port in comports():
        for manufacturer in manufacturer_scales:
            try:
                scale1 = manufacturer(port.device)
                if scale1.test_port():
                    scale1.ser.close()
                    for series in manufacturer_scales[manufacturer]:
                        try:
                            scale2 = series(port.device)
                            if scale2.test_port():
                                return scale2
                        except serial.SerialException:
                            continue
                    return scale1
                scale1.ser.close()
            except serial.SerialException:
                continue

    return None
                
class ScaleException(serial.SerialException):
    r"""Base class for all scale errors."""
    pass

class ScaleMeasurementException(ScaleException):
    r"""Raised when the scale returns an invalid measurement."""
    pass