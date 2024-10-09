from pathlib import Path

def vxlan_base(l2_vni_range, vlan_range, ASN, hostname, fabric_multi_range, fabric_rp_add):
    write_path = Path(__file__).resolve().parents[1] / "Connection" /f"{hostname}_leaf_configuration.txt"
    f = open(write_path, "a")

    formatted_commands = []
    formatted_commands.append("***** Base features Non-VPC Leaf *********\n feature nxapi\n nv overlay evpn\n feature ospf \n feature bgp \n feature pim \n feature interface-vlan \n feature vn-segment-vlan-based \n feature lacp \n feature dhcp\nfeature lldp \n feature nv overlay \n feature ngoam\n\n")
    formatted_commands.append("***** AnyCast MAC address Configuration***** \n\n fabric forwarding anycast-gateway-mac 2020.0000.00cc")
    formatted_commands.append(f"***** Multicast Configuration *****\n ip pim rp-address {fabric_rp_add} group-list {fabric_multi_range} \n ip pim ssm range 232.0.0.0/8\n\n")
    formatted_commands.append("***** Vlan Initial Configuration ***** \n")
    zipped_li = zip(l2_vni_range, vlan_range)
    for x in zipped_li:
        formatted_commands.append(f"vlan {x[1]}")
        formatted_commands.append(f"vn-segment {x[0]}")

    formatted_commands.append("****Tagging and Redistribution for Network Prefixes****\n\n route-map fabric-rmap-redist-subnet permit 10 \n match tag 12345\n\n")
    final_command = "\n".join(formatted_commands)
    f.write(final_command)
    f.close()

def l3_vni_conf(l3_vni, vrf_name, hostname, vrf_vlan):
    write_path = Path(__file__).resolve().parents[1] / "Connection" /f"{hostname}_leaf_configuration.txt"
    f = open(write_path, "a")
    ## VLAN Block ##
    description_vlan = "******* VRF VLAN Configuration *********"
    vlan_line_1 = f"vlan {vrf_vlan}"
    vlan_line_2 = f"name {vrf_name}"
    vlan_line_3 = f"vn-segment {l3_vni}"

    ## VRF Block ##
    description_block_1 = "*****L3VNI VRF Configuration****"
    line_1 = f'vrf context {vrf_name}'
    line_2 = f'description {vrf_name}'
    line_3 = f'vni {l3_vni}'
    line_4 = 'rd auto'
    line_5 = 'address-family ipv4 unicast'
    line_6 = 'route-target both auto'
    line_7 = 'route-target both auto evpn'
    line_8 = 'address-family ipv6 unicast'
    line_9 = 'route-target both auto'
    line_10 = 'route-target both auto evpn'

    formatted_commands = []
    formatted_commands.append(description_vlan)
    formatted_commands.append(vlan_line_1)
    formatted_commands.append(vlan_line_2)
    formatted_commands.append(vlan_line_3)
    formatted_commands.append(description_block_1)
    formatted_commands.append(line_1)
    formatted_commands.append(line_2)
    formatted_commands.append(line_3)
    formatted_commands.append(line_4)
    formatted_commands.append(line_5)
    formatted_commands.append(line_6)
    formatted_commands.append(line_7)
    formatted_commands.append(line_8)
    formatted_commands.append(line_9)
    formatted_commands.append(line_10)
    final_command = "\n".join(formatted_commands)
    f.write(final_command)
    f.write('\n\n')

    ### SVI Sym IRB VXLAN ##
    description_block_2 = "**** L3VNI SVI Configuration ****"
    vrf_svi_1 = f"interface Vlan{vrf_vlan}"
    vrf_svi_2 = f'description {vrf_name}'
    vrf_svi_3 = 'mtu 9216'
    vrf_svi_4 = f'vrf member {vrf_name}'
    vrf_svi_5 = 'no ip redirects'
    vrf_svi_6 = 'ip forward'
    vrf_svi_7 = 'ipv6 address use-link-local-only'
    vrf_svi_8 = 'no ipv6 redirects'
    vrf_svi_9 = 'no shut'

    formatted_commands_svi = []
    formatted_commands_svi.append(vrf_svi_1)
    formatted_commands_svi.append(vrf_svi_2)
    formatted_commands_svi.append(vrf_svi_3)
    formatted_commands_svi.append(vrf_svi_4)
    formatted_commands_svi.append(vrf_svi_5)
    formatted_commands_svi.append(vrf_svi_6)
    formatted_commands_svi.append(vrf_svi_7)
    formatted_commands_svi.append(vrf_svi_8)
    formatted_commands_svi.append(vrf_svi_9)
    formatted_commands_svi.append('\n\n')

    final_command_sv = "\n".join(formatted_commands_svi)
    f.write(final_command_sv)
    
    f.close()

def base_config(l3vni, ASN, loopback_1, loopback_2, vlans, ips, vrf_name, l2vnis, spine_loopback, hostname):
    write_path = Path(__file__).resolve().parents[1] / "Connection" /f"{hostname}_leaf_configuration.txt"
    f = open(write_path, "a")
    # SVI Block #
    zipped_vlans = zip(vlans, ips)
    formatted_commands = []
    description_block_1 = '****** SVI Configuration ******'
    formatted_commands.append(description_block_1)
    for items in zipped_vlans:
        svi_line_1 = f'interface Vlan{items[0]}'
        svi_line_2 = 'no shutdown'
        svi_line_3 = f'vrf member {vrf_name}'
        svi_line_4 = 'no ip redirects'
        svi_line_5 = f'ip address {items[1]} tag 12345'
        svi_line_6 = 'no ipv6 redirects'
        svi_line_7 = 'fabric forwarding mode anycast-gateway'
        formatted_commands.append(svi_line_1)
        formatted_commands.append(svi_line_2)
        formatted_commands.append(svi_line_3)
        formatted_commands.append(svi_line_4)
        formatted_commands.append(svi_line_5)
        formatted_commands.append(svi_line_6)
        formatted_commands.append(svi_line_7)

    formatted_commands.append('\n\n')
    # NVE Block #
    description_block_2 = '*** NVE Configuration ***'
    formatted_commands.append(description_block_2)
    formatted_commands.append("interface nve1")
    formatted_commands.append("no shutdown")
    formatted_commands.append("host-reachability protocol bgp")
    formatted_commands.append("source-interface loopback1")
    for l2vni in l2vnis:
        nve_line_1 = f'member vni {l2vni}'
        nve_line_2 = 'mcast-group 239.1.1.1'
        formatted_commands.append(nve_line_1)
        formatted_commands.append(nve_line_2)
    formatted_commands.append(f'member vni {l3vni} associate-vrf')

    formatted_commands.append('\n\n')
    description_block_3 = '**** Loopback Configuration ****'
    # Loopback Block #
    loopback_line1 = 'interface loopback0'
    loopback_line2 = 'description Routing loopback interface'
    loopback_line3 = f'ip address {loopback_1}'
    loopback_line4 = 'ip router ospf UNDERLAY area 0.0.0.0'
    loopback_line5 = 'ip pim sparse-mode'

    loopback_line6 = 'interface loopback1'
    loopback_line7 = 'description VTEP Interface'
    loopback_line8 = f'ip address {loopback_2}'
    loopback_line9 = 'ip router ospf UNDERLAY area 0.0.0.0'
    loopback_line10 = 'ip pim sparse-mode'

    formatted_commands.append(description_block_3)
    formatted_commands.append(loopback_line1)
    formatted_commands.append(loopback_line2)
    formatted_commands.append(loopback_line3)
    formatted_commands.append(loopback_line4)
    formatted_commands.append(loopback_line5)
    formatted_commands.append(loopback_line6)
    formatted_commands.append(loopback_line7)
    formatted_commands.append(loopback_line8)
    formatted_commands.append(loopback_line9)
    formatted_commands.append(loopback_line10)

    formatted_commands.append('\n\n')

    # Routing Process Block #
    description_block_4 = '***Routing process configuration***'
    formatted_commands.append(description_block_4)
    ospf_line1 = 'router ospf UNDERLAY'
    ospf_line2 = f'router-id {loopback_1[:-3]}'
    formatted_commands.append(ospf_line1)
    formatted_commands.append(ospf_line2)
    

    bgp_line1 = f'router bgp {ASN}'
    bgp_line2 = f'router-id {loopback_1[:-3]}'

    formatted_commands.append(bgp_line1)
    formatted_commands.append(bgp_line2)

    for loopback in spine_loopback:
        bgp_line3 = f'neighbor {loopback}'
        bgp_line4 = f'remote-as {ASN}'
        bgp_line5 = 'update-source loopback0'
        bgp_line6 = 'address-family l2vpn evpn'
        bgp_line7 = 'send-community'
        bgp_line8 = 'send-community extended'
        formatted_commands.append(bgp_line3)
        formatted_commands.append(bgp_line4)
        formatted_commands.append(bgp_line5)
        formatted_commands.append(bgp_line6)
        formatted_commands.append(bgp_line7)
        formatted_commands.append(bgp_line8)        

    bgp_line9 = f'vrf {vrf_name}'
    bgp_line10 = 'address-family ipv4 unicast'
    bgp_line11 = 'advertise l2vpn evpn'
    bgp_line12 = 'redistribute direct route-map fabric-rmap-redist-subnet'
    bgp_line13 = 'maximum-paths ibgp 2'

    bgp_line14 = 'address-family ipv6 unicast'
    bgp_line15 = 'advertise l2vpn evpn'
    bgp_line16 = 'redistribute direct route-map fabric-rmap-redist-subnet'
    bgp_line17 = 'maximum-paths ibgp 2'



    formatted_commands.append(bgp_line9)
    formatted_commands.append(bgp_line10)
    formatted_commands.append(bgp_line11)
    formatted_commands.append(bgp_line12)
    formatted_commands.append(bgp_line13)
    formatted_commands.append(bgp_line14)
    formatted_commands.append(bgp_line15)
    formatted_commands.append(bgp_line16)
    formatted_commands.append(bgp_line17)
    formatted_commands.append('evpn')
    ## EVPN Add ##
    for l2vni in l2vnis:
        formatted_commands.append(f'vni {l2vni} l2')
        formatted_commands.append('rd auto')
        formatted_commands.append('route-target import auto')
        formatted_commands.append('route-target export auto')
    formatted_commands.append('\n\n')

    final_command = "\n".join(formatted_commands)
    f.write(final_command)
    f.close()


def interface_config(fabric_addresses, fabric_interfaces, hostname):
    write_path = Path(__file__).resolve().parents[1] / "Connection" /f"{hostname}_leaf_configuration.txt"
    f = open(write_path, "a")
    formatted_commands = []
    formatted_commands.append('**** Fabric Underlay Configuration ****\n\n')
    fabric_all = zip(fabric_addresses, fabric_interfaces)
    formatted_commands = []
    for x in fabric_all:
        
        formatted_commands.append(f'interface {x[1]}')
        formatted_commands.append('no switchport')
        formatted_commands.append('mtu 9216')
        formatted_commands.append(f'ip address {x[0]}')
        formatted_commands.append('ip ospf network point-to-point')
        formatted_commands.append('ip router ospf UNDERLAY area 0.0.0.0')
        formatted_commands.append('ip pim sparse-mode')
        formatted_commands.append('no shutdown \n\n')



    final_command = "\n".join(formatted_commands)
    f.write(final_command)
    f.close()