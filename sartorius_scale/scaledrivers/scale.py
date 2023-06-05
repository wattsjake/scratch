import serial

# Superclass for all scales

class Scale:

    timeout = 0.5  # Default timeout for serial communication

    # This was made by Noah Mazza.
    def __init__(self):
        if not 'PRINT_SCREEN' in locals():
            self.set_print_screen(b'SI\r\n')  # For testing Mettler Toledo scales

    # def __init__(self, port_, baudrate_, bytesize_, stopbits_, parity_, timeout_):
    #     self.ser = serial.Serial(port = port_, baudrate = baudrate_, bytesize = bytesize_, stopbits = stopbits_, parity = parity_, timeout = timeout_)
    #     return self

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

    def set_serial(self, port_: str, *args):

        if isinstance(args[0], dict):
            self.ser = serial.Serial(port=port_, 
                                     baudrate = args[0].get("baudrate", 9600), 
                                     bytesize = args[0].get("bytesize", serial.EIGHTBITS), 
                                     stopbits = args[0].get("stopbits", serial.STOPBITS_ONE), 
                                     parity = args[0].get("parity", serial.PARITY_NONE), 
                                     timeout = self.timeout)
            
        else:
            self.ser = serial.Serial(port=port_,
                                     baudrate = (args[0:1]+(9600,))[0],
                                     bytesize = (args[1:2]+(serial.EIGHTBITS,))[0],
                                     stopbits = (args[2:3]+(serial.STOPBITS_ONE,))[0],
                                     parity = (args[3:4]+(serial.PARITY_NONE,))[0],
                                     timeout = self.timeout)
        
        return self


    # # # GETTERS # # #
    # Will fill in later as needed


    # # # METHODS # # #

    # This method is used to send a command to the scale and receive a response.
    # After sending a command, the response has to be read or else miscommunication will occur.
    def send_receive(self, command):
        self.ser.write((self.COMMAND_START + command + self.COMMAND_END).encode('utf-8'))
        return self.ser.readline()

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
    
manufacturers = {"Sartorius": sartorius, 
                 "Mettler Toledo": mettlertoledo}  # Dictionary of all possible manufacturers

# Dictionary of all scales by manufacturer
manufacturer_scales = {sartorius: sartorius.scales,
                       mettlertoledo: mettlertoledo.scales}