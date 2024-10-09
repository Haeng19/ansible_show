import re
import socket

def validate_device_type(device_type):
    if device_type == "cisco_nxos":
        pass
    else:
        raise Exception("This is an incorrect device type")


def validate_patt_li(test_strings):
    ref_pattern = re.compile("^[a-zA-Z0-9!@#$%^&*()_+=-]+$")
    for string in test_strings:
        if ref_pattern.match(string):
            pass
        else:
            raise Exception("Given input must contain the following characters: a-zA-Z0-9!@#$%^&*()_+=-")


## Val IPs ##
def validate_ip(IP_address):
    try:
        socket.inet_aton(IP_address)
        pass
    except:
        raise Exception("IP address does not follow the correct format")

def validate_list(list_of_ips):
    for i in list_of_ips:
        try:
            socket.inet_aton(i)
            pass
        except:
            raise Exception("IP address does not follow the correct format")
    

def validate_name_sin(hostname):
    ref_pattern = re.compile("^[a-zA-Z0-9-_]+$")
    if ref_pattern.match(hostname):
        pass
    else:
        raise Exception("Hostname name must only contain the characters a-zA-Z0-9-_")