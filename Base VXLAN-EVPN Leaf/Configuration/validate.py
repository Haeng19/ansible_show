import re
import socket

def validate_vni(l2_vnis):
    l2_vni_expected = []    
    # Ints in #
    for i in l2_vnis:
        if i.isdigit() is True:
            l2_vni_expected.append(int(i))
        else:
            raise Exception("Vnis must be valid integers between 1 to 16777215")
    
    # Check ran for Vxlan 1 to 16777215 # 
    for s in l2_vni_expected:
        if s in range( 1 , 16777215):
            pass
        else:
            raise Exception("Vnis must be valid integers between 1 to 16777215")



def validate_vlan(vlans):
    vlans_expected = []

    # Ints in #
    for i in vlans:
        if i.isdigit() is True:
            vlans_expected.append(int(i))
        else: 
            raise Exception("Vlans must be valid integers between 1 to 4094")
    
    # Check ran for Vlan 1 to 4094
    for s in vlans_expected:
        if s in range( 1, 4094):
            pass
        else:
            raise Exception("Vlans must be valid integers between 1 to 4094")

def validate_vlan_sin(vlan_id):
    if isinstance(vlan_id, int) and vlan_id in range(1, 4094):
        pass
    else:
        raise Exception("Vlan expected to be in the range 1 to 4094")


def validate_l3_vni(l3vni):
    if isinstance(l3vni, int) and l3vni in range(1 , 16777215):
        pass
    else:
        raise Exception("L3vni must be a valid integer and between 1 to 16777215")


def validate_name(vrf_name , hostname):
    ref_pattern = re.compile("^[a-zA-Z0-9-_]+$")
    if ref_pattern.match(vrf_name):
        pass
    else:
        raise Exception("Vrf name must only contain the characters a-zA-Z0-9-_")
    
    if ref_pattern.match(hostname):
        pass
    else:
        raise Exception("Hostname must only contain the characters a-zA-Z0-9-_")


def validate_asn(ASN):
    if isinstance(ASN, int) and ASN in range(1 , 65535):
        pass
    else:
        raise Exception("ASN must be a valid integer and between 1 to 65535")

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

def validate_list_cidr(list_of_cidrs):
    ip_cidr_pattern = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(3[0-2]|[12]?[0-9])$")
    for ip_cidr in list_of_cidrs:
        if ip_cidr_pattern.match(ip_cidr):
            pass
        else:
            raise Exception("Given address must be in an <IP>/<CIDR> notation")


def validate_sin_cidr(cidr_add):
    ip_cidr_pattern = re.compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(3[0-2]|[12]?[0-9])$")
    
    if ip_cidr_pattern.match(cidr_add):
        pass
    else:
        raise Exception("Given address must be in an <IP>/<CIDR> notation")


## Val interface ##

def validate_interface_list(interfaces):
    int_pattern = re.compile("^[a-zA-Z0-9/]+$")
    for interface in interfaces:
        if int_pattern.match(interface):
            pass
        else:
            raise Exception("Interface ID must only contain the characters a-zA-Z0-9/")


def validate_name_sin(hostname):
    ref_pattern = re.compile("^[a-zA-Z0-9-_]+$")
    if ref_pattern.match(hostname):
        pass
    else:
        raise Exception("Hostname name must only contain the characters a-zA-Z0-9-_")