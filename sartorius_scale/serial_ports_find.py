from serial.tools.list_ports import comports
from scaledrivers import scale, mettlertoledo, sartorius
from scaledrivers.scale import Scale

# port_list stores the actual com port
port_list = comports()

# Each vendor's product ids matched to the product
SARTORIUS_PID_LIST = {"vendor": "Sartorius",
                      16: "EntrisII",
                      24577: "EntrisII"}

# All scale vendor ids linked to the vendor
VID_LIST = {9404: SARTORIUS_PID_LIST,
            1027: SARTORIUS_PID_LIST}

# Every product matched to its driver
PRODUCT_DRIVERS = {"Entris": Scale,
                   "Entris_II": sartorius.EntrisII}

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
    if baud == "":
        baud = 9600
    bits = input("Enter the number of bits: ")
    if bits == "":
        bits = 8
    stop_bits = input("Enter the number of stop bits: ")
    if stop_bits == "":
        stop_bits = 1
    parity = input("Enter the parity: ")
    if parity == "":
        parity = "N"
    scale = Scale()
    scale.set_serial(com, baud, bits, stop_bits, parity, 2)
    return scale

# scale = connect_scale()

# if(scale != None):
#     print("Scale Connected")
#     print(scale.ser)

#     while(True):
#         print(scale.read_screen().decode('utf-8'))

# else:
#     print("Scale not connected")

