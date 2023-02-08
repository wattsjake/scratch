import serial

class Scale:

    # This was made by Noah Mazza.

    BAUDRATES = None
    BYTESIZES = None
    STOPBITS = None
    PARITIES = None

    DEFAULT = None

    TARE = None
    PRINT_SCREEN = None
    ZERO = None
    SOUND = None

    # All of this was generated with GitHub Copilot.  We'll see if it works.

    def __init__(self, port):
        print(self.BAUDRATES)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ser.close()

    def get(self):
        self.ser.write(b'P\r')
        return self.ser.readline()

    def zero(self):
        self.ser.write(b'Z\r')

    def tare(self):
        self.ser.write(b'T\r')

    def get_info(self):
        self.ser.write(b'V\r')
        return self.ser.readline()

    def get_stability(self):
        self.ser.write(b'S\r')
        return self.ser.readline()

    def get_units(self):
        self.ser.write(b'U\r')
        return self.ser.readline()

    def get_mass(self):
        self.ser.write(b'P\r')
        return self.ser.readline()

    def get_status(self):
        self.ser.write(b'ST\r')
        return self.ser.readline()

    def get_error(self):
        self.ser.write(b'ER\r')
        return self.ser.readline()

    def get_battery(self):
        self.ser.write(b'BT\r')
        return self.ser.readline()

    def get_temperature(self):
        self.ser.write(b'TM\r')
        return self.ser.readline()

    def get_calibration(self):
        self.ser.write(b'CL\r')
        return self.ser.readline()

    def get_calibration_date(self):
        self.ser.write(b'CD\r')
        return self.ser.readline()

    def get_calibration_time(self):
        self.ser.write(b'CT\r')
        return self.ser.readline()

    def get_calibration_user(self):
        self.ser.write(b'CU\r')
        return self.ser.readline()

    def get_calibration_weight(self):
        self.ser.write(b'CW\r')
        return self.ser.readline()

    def get_calibration_weight_units(self):
        self.ser.write(b'CU\r')
        return self.ser.readline()