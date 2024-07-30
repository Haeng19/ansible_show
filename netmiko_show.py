# Import modules

from netmiko import ConnectHandler
import getpass

command = input("Enter the IOS-XE router show command you want to display?")
username = input("Provide a username: ")
password = getpass.getpass('Provide a password: ')

routers = ["192.168.122.19", "192.168.122.20"]

def call_play():
	for x in routers:
		router = {'device_type':'cisco_xe', 'host':x, 'username':username, 'password':password}
		router_connect = ConnectHandler(**router)
		router_connect.send_command("terminal length 0")
		hostname = router_connect.send_command("show run | include hostname").split()[1]
		print(f"This is the output for {hostname} find below")
	        output = router_connect.send_command(command)
		print(output)
		print()
		router_connect.disconnect()
		



#################### Part two  ###################################

from netmiko import ConnectionHandler
import getpass
import netmiko.ssh_exception import AuthenticationException
import netmiko.ssh_exception import NetworkTimeoutException
import os

os.chdir("/roots/Scripts")  # get to the directory

username = input("Provide a username: ")
password = getpass.getpass('Provide a password: ')

routers = ["192.168.122.19", "192.168.122.20"]
call_play()

def call_play():
	for x in routers:
		try:
			router_connect = ConnectHandler(**router)
			router = {'device_type':'cisco_xe', 'host':x, 'username':username, 'password':password}
		except(AuthenticationException):
			print(f"Authentication Failure: {x} ")
			continue
		except(NetworkTimeoutException):
			print(f"Timeout to device: {x} ")
			continue
		router_connect.send_command("terminal length 0")
		hostname = router_connect.send_command("show run | include hostname").split()[1]
		print("*******Connecting to device: {hostname}***********")
	        output = router_connect.send_command("show run")
		file = open(f'{hostname}.cfg', 'w') 
		file.write(output)
		file.close()
		print("*********Copying config for : {hostname}*******\n")	
		# open file pointer
		router_connect.disconnect()
	
				
