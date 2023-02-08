from serial.tools.list_ports import comports
from serial_type_a_usb import Entris

# port_list stores the actual com port
port_list = comports()

# Each vendor's product ids matched to the product
SARTORIUS_PID_LIST = {"vendor": "Sartorius", 
                      8963: "Entris"}

# All scale vendor ids linked to the vendor
VID_LIST = {1659: SARTORIUS_PID_LIST}

# Every product matched to its driver
PRODUCT_DRIVERS = {"Entris": Entris}

# Define the scale
scale = None;

for port in port_list:
    print(port)
    print(port.vid)
    print(port.pid)

    # If the vendor id is in the list of vendors, store vendor information and possible product ids
    if(port.vid in VID_LIST):
        vendor_pid_list = VID_LIST[port.vid]  # Stores possible product ids for that vendor
        vendor = vendor_pid_list["vendor"]  # Stores the name of the vendor
        print("Found " + vendor + " Product")

        # If the product id is in the list of product ids for that vendor, 
        # [TODO] Connect to the product using the driver
        if(port.pid in vendor_pid_list):
            product = vendor_pid_list[port.pid]  # Stores the name of the product
            print("Found " + product + " Scale")
            print(port.device)
            scale = PRODUCT_DRIVERS[product]()

            
        else:
            print("Scale not found")




