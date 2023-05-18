
# Automation script to create vlans and assign switchports at a L2 switch
from netmiko import ConnectionHandler

# First is to define the inventory

testSW2 = {
    'device_type' : 'cisco_ios',
    'host' : '192.168.1.1',
    'username' : 'xxxx',
    'password' : 'xxxx',
    'secret' : 'xxxx'
}

testSW1 = {
    'device_type' : 'cisco_ios',
    'host' : '192.168.1.2',
    'username' : 'xxxx',
    'password' : 'xxxx',
    'secret' : 'xxxx'

}

# Next is to establish an SSH connections to both hosts

testSW1_connect = ConnectionHandler(**testSW1)
testSW2_connect = ConnectionHandler(**testSW2)

# Send the appropriate commands to the switches

config_commands = ['vlan 10',
                   'name netmiko_test1',
                   'exit',
                   'vlan 20',
                   'name netmiko_test2',
                   'exit'
                   ]

# Commit the commands to the switches

set_output_testSW1 = testSW1_connect.send_config_set(config_commands)
set_output_testSW2 = testSW2_connect.send_config_set(config_commands)

# Print the output to verify that the correct commands have been send the switches

print(set_output_testSW1)
print(set_output_testSW2)

# Send verification command to ensure the vlan database has been set correctly

verify_output_testSW1 = testSW1_connect.send_command('sh vlan bri')
verify_output_testSW2 = testSW2_connect.send_command('sh vlan bri')

# print out both commands to the console to ensure they have been applied correctly

print(verify_output_testSW1)
print(verify_output_testSW2)

# Assign the interfaces to the newly created vlans

interface_commands = ['interface fa0/1',
                      'switchport mode access',
                      'switchport access vlan 10',
                      'interface fa0/2',
                      'switchport mode access',
                      'switchport access vlan 20'
                      ]

set_interface_testSW1 = testSW1_connect.send_config_set(interface_commands)
set_interface_testSW2 = testSW2_connect.send_config_set(interface_commands)

# print the commands to ensure that the correct commands have been inputted

print(set_interface_testSW1)
print(set_interface_testSW2)

# verify the interfaces have been set

verify_interface_testSW1 = testSW1_connect.send_command('sh run interface fa0/1')
verify_interface_testSW2 = testSW2_connect.send_command('sh run interface fa0/2')

# print out both command to the console to ensure they have been applied correctly

print(verify_interface_testSW1)
print(verify_interface_testSW2)