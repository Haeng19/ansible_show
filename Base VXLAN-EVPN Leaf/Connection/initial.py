from netmiko import ConnectHandler
from validate import validate_device_type, validate_ip, validate_patt_li, validate_name_sin
from User_in import get_devices
from pathlib import Path
import csv

class Device:
    all = []
    def __init__(self, device_type:str, ip: str, username:str, password: str, hostname:str):

        # Once vali , go through the Assi #
        validate_device_type(device_type)
        validate_ip(ip)
        validate_patt_li([username, password])
        validate_name_sin(hostname)


        # Inital Assi #
        self.device_type = device_type
        self.ip = ip
        self.username  = username
        self.password = password
        self.hostname = hostname

        # Add to all #
        Device.all.append(self)


    # Get devices from CSV    
    @classmethod
    def instantiate_from_csv(cls):
        csv_file_device, password = get_devices()
        file_csv = csv_file_device + ".csv"
        file_path = Path(__file__).parent / file_csv
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            devices_list = list(reader)
        for devices in devices_list:
            Device(devices.get('Device_type'), devices.get('IP_Address'), devices.get('username'), password, devices.get('hostname'))


    ## Magic method to return the attributes ##
    def __repr__(self):
        return f"{self.device_type}, {self.ip}, {self.username}, {self.password}, {self.hostname}"

Device.instantiate_from_csv()

# Retrive Obj #
# CLI into #

All_devices =  []
for device in Device.all:
    All_devices.append({"device_type": device.device_type, "ip": device.ip, "username": device.username, "password": device.password, "hostname": device.hostname })

for device in All_devices:
    net_connect = {
        "device_type": device.get("device_type"),
        "ip":device.get("ip"),
        "username":device.get("username"),
        "password":device.get("password")
    }
    con_to = ConnectHandler(**net_connect)
    hostname = device.get("hostname")
    file_path = Path(__file__).parent / f"{hostname}_leaf_configuration.txt"
    with open(file_path) as poi:
        config_leaf = poi.read().splitlines()
    
    output_printed = con_to.send_config_set(config_leaf)
    print(output_printed)




