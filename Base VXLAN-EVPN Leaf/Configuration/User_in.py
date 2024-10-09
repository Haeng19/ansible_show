def get_all(hostname):
    csv_spine = input(f"Give me the csv file name for the Spine Loopbacks (do not include the extension) for {hostname}: ")
    csv_fabric_params = input(f"Give me the csv file name which contains the fabric parameter for {hostname}: ")
    csv_file_fabric = input(f"Give me the csv file name for the Fabric Links (do not include the extension) for {hostname}: ")
    csv_file = input(f"Give me the csv file name for VNI-VLAN Mappings (do not include the extension) for {hostname}: ")
    csv_file_vlan_l3 = input(f"Give me the csv file name for VLAN-IP Mappings (do not include the extension) for {hostname}: ")
    print("\n")
    return csv_file, csv_file_vlan_l3, csv_file_fabric, csv_spine, csv_fabric_params