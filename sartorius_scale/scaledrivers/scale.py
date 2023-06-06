import serial
import fastnumbers as fn

# Superclass for all scales

class Scale:
    r"""Superclass for all scales.

    Stores a collection of methods and attributes that are common to all scales.

    """

    TIMEOUT = 0.1  # Default timeout for serial communication

    # This was made by Noah Mazza.
    def __init__(self, **kwargs):
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

    def set_serial(self, port_: str, *args, **kwargs) -> serial.Serial:
        r"""Sets the serial port for the scale.

        Args:
            port_ (str): Name of port to connect to.
            *args[0] (dict, optional): Dictionary of keyword arguments for the serial connection.
            **baudrate (int, optional): Baudrate for serial connection. Default is 9600.
            **bytesize (int, optional): Bytesize for serial connection. Default is serial.EIGHTBITS.
            **stopbits (int, optional): Stopbits for serial connection. Default is serial.STOPBITS_ONE.
            **parity (int, optional): Parity for serial connection. Default is serial.PARITY_NONE.

        Returns:
            serial.Serial: Serial connection made by scale.
        """        

        args[0].update(kwargs)  # kwargs override args[0] if they share a key

        self.ser = serial.Serial(port=port_, 
                                 baudrate = args[0].get("baudrate", 9600), 
                                 bytesize = args[0].get("bytesize", serial.EIGHTBITS), 
                                 stopbits = args[0].get("stopbits", serial.STOPBITS_ONE), 
                                 parity = args[0].get("parity", serial.PARITY_NONE), 
                                 timeout = args[0].get("timeout", self.TIMEOUT))
        
        return self.ser


    # # # GETTERS # # #
    # Will fill in later as needed


    # # # METHODS # # #

    # This method is used to send a command to the scale and receive a response.
    # After sending a command, the response has to be read or else miscommunication will occur.
    def send_receive(self, command: str) -> str:
        r"""Send a command and receive the scale's response.

        Commands are automatically encoded and responses are automatically decoded.
        Check the scale's documentation for a list of commands.

        Args:
            command (str): Command to send to the scale.

        Returns:
            str: The scale's response to the command.
        """
        
        self.ser.write((self.COMMAND_START + command + self.COMMAND_END).encode(self.encoding))
        return self.ser.readline().decode(self.encoding)

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
    
# Dictionary of all possible manufacturers
manufacturers = {"Sartorius": sartorius, 
                 "Mettler Toledo": mettlertoledo}  

# Dictionary of all scales by manufacturer
manufacturer_scales = {sartorius: sartorius.scales,
                       mettlertoledo: mettlertoledo.scales}

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