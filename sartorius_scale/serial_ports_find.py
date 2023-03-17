from serial.tools.list_ports import comports
from serial_type_a_usb import Entris
from serial_type_c_usb import Entris_II
import serial
from scale_superclass import Scale

# port_list stores the actual com port
port_list = comports()

# Each vendor's product ids matched to the product
SARTORIUS_PID_LIST = {"vendor": "Sartorius",
                      16: "Entris_II",
                      24577: "Entris_II"}

# All scale vendor ids linked to the vendor
VID_LIST = {9404: SARTORIUS_PID_LIST,
            1027: SARTORIUS_PID_LIST}

# Every product matched to its driver
PRODUCT_DRIVERS = {"Entris": Entris,
                   "Entris_II": Entris_II}

# Define the scale
scale = None;

# connect_scale() connects to the scale
def connect_scale():
    for port in port_list:

        # Print the port information for testing purposes
        print(port)
        print(port.vid)
        print(port.pid)

        # If the vendor id is in the list of vendors, store vendor information and possible product ids
        if(port.vid in VID_LIST):
            vendor_pid_list = VID_LIST[port.vid]  # Stores possible product ids for that vendor
            vendor = vendor_pid_list["vendor"]  # Stores the name of the vendor
            print("Found " + vendor + " Product")

            # If the product id is in the list of product ids for that vendor, 
            if(port.pid in vendor_pid_list):
                product = vendor_pid_list[port.pid]  # Stores the name of the product
                print("Found " + product + " Scale")
                print(port.device)

                # Connect to the scale using the proper subclass to allow communications with that specific scale
                scale = PRODUCT_DRIVERS[product](port.device)

                scale.sound()  # Test the scale

                # Return the connected scale
                return scale

                
            else:
                print("Scale not found")
        
    return None

def custom_connect_scale():
    print("Custom Scale Connection")
    com = input("Enter the com port: ")
    baud = input("Enter the baud rate: ")
    bits = input("Enter the number of bits: ")
    stop_bits = input("Enter the number of stop bits: ")
    parity = input("Enter the parity: ")
    scale = Scale(com, baud, bits, stop_bits, parity, 2)

# scale = connect_scale()

# if(scale != None):
#     print("Scale Connected")
#     print(scale.ser)

#     while(True):
#         print(scale.read_screen().decode('utf-8'))

# else:
#     print("Scale not connected")

