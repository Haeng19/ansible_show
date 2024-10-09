from validate import validate_vlan, validate_vni, validate_l3_vni, validate_name, validate_asn, validate_name_sin, validate_list_cidr, validate_ip, validate_interface_list, validate_sin_cidr, validate_list
from config_base import vxlan_base, l3_vni_conf, base_config, interface_config
from User_in import get_all
import csv
from pathlib import Path


class vxlan_evpn_leaf:
    def __init__(self, l2_vni_range : list, vlan_range : list, l3_vni : int, vrf_name: str, vrf_vlan: int ,ASN: int, hostname: str, loopback_1: str, loopback_2: str, fabric_addresses: list, 
                 fabric_interfaces: list, vlan_ids: list, IPs: list, spine_loopback: list, fabric_multi_range: str, fabric_rp_add: str):

        # Assign params to inital obj #
        self.l2_vni_range = l2_vni_range
        self.vlan_range = vlan_range
        self.l3_vni = l3_vni
        self.vrf_name = vrf_name
        self.vrf_vlan = vrf_vlan
        self.ASN = ASN
        self.loopback_1 = loopback_1
        self.loopback_2 = loopback_2
        self.fabric_addresses = fabric_addresses
        self.fabric_interfaces = fabric_interfaces
        self.vlan_ids = vlan_ids
        self.IPs = IPs
        self.fabric_multi_range = fabric_multi_range
        self.fabric_rp_add = fabric_rp_add


        # Validate params # 
        validate_vni(l2_vni_range)
        validate_vlan(vlan_range)
        validate_l3_vni(l3_vni)
        validate_name(vrf_name, hostname)
        validate_asn(ASN)
        validate_list(spine_loopback)
        validate_ip(fabric_rp_add)
        validate_sin_cidr(fabric_multi_range)
        # Sep CSV
        validate_vlan(vlan_ids)
        validate_list_cidr(IPs)
        
        ip_list = [loopback_1, loopback_2]
        validate_list_cidr(ip_list)
        validate_list_cidr(fabric_addresses)
        validate_interface_list(fabric_interfaces)

        # Once val open file for conf #
        write_path = Path(__file__).resolve().parents[1] / "Connection" /f"{hostname}_leaf_configuration.txt"
        
        f = open(write_path, "w")
        f.close()

        # Generate config
        vxlan_base(l2_vni_range, vlan_range, ASN, hostname, fabric_multi_range, fabric_rp_add)
        l3_vni_conf(l3_vni, vrf_name, hostname, vrf_vlan)
        base_config(l3_vni, ASN, loopback_1, loopback_2, vlan_ids, IPs, vrf_name, l2_vni_range, spine_loopback, hostname)
        interface_config(fabric_addresses, fabric_interfaces, hostname)


    
    @classmethod
    def instantiate_from_csv(cls, hostname:str):
        validate_name_sin(hostname)
        # Get specific
        csv_file, csv_file_vlan, csv_file_fabric, csv_spine, csv_fabric_params = get_all(hostname)

        ## VNI-VLAN ##

        file_1 = csv_file + ".csv"
        filepath_1 = Path(__file__).parent / hostname /file_1
        with open(filepath_1, 'r') as f:
            reader = csv.DictReader(f)
            all_list = list(reader)
        f.close()
        l2vnis = []
        vlans = []
        for item in all_list:
            l2vnis.append(item.get('L2VNI'))
            vlans.append(item.get('VLAN'))
        

        ## VLAN-IP ##
        file_2 = csv_file_vlan + ".csv"
        filepath_2 = Path(__file__).parent / hostname/ file_2
        with open(filepath_2 , 'r') as fv:
            reader_vlan = csv.DictReader(fv)
            vlan_list = list(reader_vlan)
        fv.close()

        vlan_id = []
        ip_addresses = []
        for terms in vlan_list:
            vlan_id.append(terms.get('Vlan_ID'))
            ip_addresses.append(terms.get('IP_Address'))
        

        ## Fab Underlay ##
        file_3 = csv_file_fabric + ".csv"
        filepath_3 = Path(__file__).parent / hostname / file_3
        with open(filepath_3, 'r') as ff:
            reader_fabric = csv.DictReader(ff)
            fabric_list = list(reader_fabric)

        fabric_addresses = []
        fabric_interfaces = []
        for m in fabric_list:
            fabric_addresses.append(m.get("IP_Address"))
            fabric_interfaces.append(m.get("Interfaces"))
        
        file_4 = csv_fabric_params + ".csv"
        filepath_4 = Path(__file__).parent / hostname / file_4
        
        with open(filepath_4, 'r') as fm:
            reader_multi = csv.DictReader(fm)
            fabric_list = list(reader_multi)
        
        for mm in fabric_list:
            fabric_rp_add = mm.get("RP_Address")
            fabric_multi_range = mm.get("Multicast_Range")
            l3_vni = int(mm.get("L3VNI"))
            vrf_name = mm.get("VRF_Name")
            vrf_vlan = mm.get("VRF_VLAN")
            ASN = int(mm.get("ASN"))
            loopback_1 = mm.get("Routing_Loopback")
            loopback_2 = mm.get("VTEP_Loopback")

        
        file_5 = csv_spine + ".csv"
        filepath_5 = Path(__file__).parent / hostname / file_5
        with open(filepath_5, 'r') as fs:
            reader_spine = csv.DictReader(fs)
            spine_list = list(reader_spine)
        spine_loopback = []
        for loopback in spine_list:
            spine_loopback.append(loopback.get("Spine_Loopback"))

        vxlan_evpn_leaf(l2vnis, vlans, l3_vni, vrf_name, vrf_vlan, ASN, hostname, loopback_1, loopback_2, fabric_addresses, fabric_interfaces,vlan_id, ip_addresses, spine_loopback, fabric_multi_range, fabric_rp_add)


# Initial for all
def init():    
        # Get the devices #
    file_device = "Devices.csv"
    filepath_devices = Path(__file__).parent/ file_device
    with open(filepath_devices, 'r') as dd:
        reader_devices = csv.DictReader(dd)
        all_devices = list(reader_devices)
    # Extract
    for device in all_devices:
        vxlan_evpn_leaf.instantiate_from_csv(device.get("hostname"))

# invoke #
init()