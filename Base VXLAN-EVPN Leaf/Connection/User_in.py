from getpass import getpass
def get_devices():
    csv_file = input("Type in the csv file which contains the devices: ")
    password = getpass("Type in a password to gain CLI access: ")
    return csv_file, password