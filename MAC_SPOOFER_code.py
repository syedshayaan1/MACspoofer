# SYED SHAYAAN HASNAIN AHMAD
# 20I-0647
# SECTION B
# ETHICAL HACKING PROJECT


# IMPORTING RELEVANT LIBRARIES

import subprocess
import re
import subprocess
import string
import random
import re
import json
import os
import platform
from datetime import datetime

#registry path of network interfaces : This variable stores the registry path for network interfaces on Windows.
network_interface_reg_path = r"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}"


# These regular expressions are used to match and extract transport names and MAC addresses.

# Transport name regular expression
transport_name_regex = re.compile("{.+}")

# MAC address regular expression
mac_address_regex = re.compile(r"([A-Z0-9]{2}[:-]){5}([A-Z0-9]{2})")

# Checking platform
p=""
if platform.system().lower() == "windows":
    p = "win"
else:
    p = "linux"
    
# 30 companies along with their OUIs
OUI = {

    'Microsoft': "70:F8:AE",
    'Dell': "D0:43:1E",
    'HP': "64:4E:D7",
    'Samsung': "64:1B:2F",
    'Apple': "60:FD:A6",
    'Google': "60:70:6C",
    'Lenovo': "48:C3:5A",
    'Sony': "F4:64:12",
    'IBM': "40:F2:E9",
    'Asus': "00:26:18",
    'Acer': "18:06:FF",
    'Intel': "E4:C7:67",
    'Nvidia': "48:B0:2D",
    'AMD': "74:27:2C",
    'Amazon': "84:28:59",
    'Cisco': "E8:0A:B9",
    'Oracle': "00:21:F6",
    'Realme': "5C:A0:6C",
    'Honor': "0C:B9:83",
    'OPPO': "E4:40:97",
    'OnePlus': "AC:C0:48",
    'Nokia': "28:6F:B9",
    'HTC': "40:4E:36",
    'LG': "AC:5A:F0",
    'Huawei': "E0:06:30",
    'Blackberry': "48:9D:24",
    'Alcatel': "88:3C:93",
    'ZTE': "F0:1B:24",
    'Infinix': "E8:C2:DD",
    'Tecno': "4C:A3:A7"
}

OUI_list = list(OUI.items())

# Function to perform network scanning and list connected devices' MAC addresses

def scan_network():
    try:
        # Perform ARP scanning to discover devices on the network
        arp_output = subprocess.check_output(["arp", "-a"]).decode()

        # Regular expression pattern to extract IP and MAC addresses
        pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+([0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})")

        # Extract IP and MAC addresses from ARP output
        devices = pattern.findall(arp_output)

        # Display the list of connected devices' MAC addresses
        print("Connected Devices' MAC Addresses:")
        for ip, mac in devices:
            print(f"IP Address: {ip}, MAC Address: {mac}")

    except subprocess.CalledProcessError as e:
        print("Error scanning the network:", e)



# function to save mac address to a file
def save_mac_addresses_to_file(mac_dict, filename='mac_addresses.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(mac_dict, file)
        print(f"MAC addresses saved to {filename}")
    except Exception as e:
        print(f"Error saving MAC addresses to {filename}: {e}")

# function to read mac addresses from a file
def read_mac_addresses_from_file(filename='mac_addresses.json'):
    try:
        with open(filename, 'r') as file:
            mac_dict = json.load(file)
        print(f"MAC addresses loaded from {filename}")
        return mac_dict
    except Exception as e:
        print(f"Error reading MAC addresses from {filename}: {e}")
        return None

# function to get the mac addresses on windows
def get_mac_addresses_win():
    try:
        #make a list to collect connected adapter's MAC addresses along with the transport name
        connected_adapters_mac = []
        #use the getmac command to extract 
        for potential_mac in subprocess.check_output("getmac").decode().splitlines():
            #parse the MAC address from the line
            mac_address = mac_address_regex.search(potential_mac)
            #parse the transport name from the line
            transport_name = transport_name_regex.search(potential_mac)
            if mac_address and transport_name:
                #if a MAC and transport name are found, add them to the list
                connected_adapters_mac.append((mac_address.group(), transport_name.group()))
        return connected_adapters_mac
    except subprocess.CalledProcessError:
        print("Error retrieving MAC addresses.")
        return None
    
# function to get mac addresses on linux
    
def get_mac_addresses_linux():
    try:
        #run ifconfig command
        result = subprocess.check_output(["ifconfig", "-a"]).decode("utf-8")
        #get interfaces
        interfaces = re.findall(r"(\w+):", result)
        #get mac addresses
        mac_addresses = re.findall(r"(\w+:\w+:\w+:\w+:\w+:\w+)", result)
        return dict(zip(interfaces, mac_addresses))
    except subprocess.CalledProcessError:
        print("Error retrieving MAC addresses.")
        return None

# function to display the mac addresses on windows
    
def display_mac_addresses_win(connected_adapters_mac):
    for i, option in enumerate(connected_adapters_mac):
        print(f"{i}. {option[0]}")

# function to display the mac addresses on linux
def display_mac_addresses_linux(mac_dict):
    if mac_dict:
        print("MAC Address(es):")
        for interface, mac_address in mac_dict.items():
            mac_address = mac_address.upper()
            print(f"{interface}, {mac_address}")
    else:
        print("No MAC addresses found.")

# function to clean non hex characters and remove - and : from mac addresses
def clean_mac(mac):
    return "".join(c for c in mac if c in string.hexdigits).upper()

# function to disable an adapter
def disable_adapter(adapter_index):
    # wmic command to disable adapter so the MAC address change is reflected
    disable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call disable").decode()
    return disable_output

# function to enable an adapter
def enable_adapter(adapter_index):
    #wmic command to enable adapter so the MAC address change is reflected
    enable_output = subprocess.check_output(f"wmic path win32_networkadapter where index={adapter_index} call enable").decode()
    return enable_output

# function to GENERATE RANDOM MAC address on windows

def get_random_mac_address_win():
    #hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    #2nd character must be 2, 4, A, or E
    return random.choice(uppercased_hexdigits) + random.choice("24AE") + "".join(random.sample(uppercased_hexdigits, k=10))
       
# function to GENERATE RANDOM MAC address on linux

def get_random_mac_address_linux():
    #hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    #2nd character must be 0, 2, 4, 6, 8, A, C, or E
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")

# function to generate a random mac address on windows with a specfied manufacturers OUI

def generate_random_mac_with_oui_win(oui_prefix):
    #hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    #remaining part of the MAC address
    remaining_part = ''.join(random.choice(uppercased_hexdigits) for _ in range(6))
    #concatenate the OUI prefix and the remaining part
    mac_address = f"{oui_prefix[0:6]}{remaining_part[0:6]}"
    return mac_address

# function to generate a random mac address on linux with a specfied manufacturers OUI
def generate_random_mac_with_oui_linux(oui_prefix):
    #hexdigits uppercased
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    #remaining part of the MAC address
    remaining_part = ''.join(random.choice(uppercased_hexdigits) for _ in range(6))
    #concatenate the OUI prefix and the remaining part
    mac_address = f"{oui_prefix[:2]}:{oui_prefix[2:4]}:{oui_prefix[4:6]}:{remaining_part[:2]}:{remaining_part[2:4]}:{remaining_part[4:]}"
    return mac_address

# functoin to CHANGE MAC address on windows

def change_mac_address_win(adapter_transport_name, new_mac_address):
    #reg QUERY command to get available adapters from the registry
    output = subprocess.check_output(f"reg QUERY " +  network_interface_reg_path.replace("\\\\", "\\")).decode()
    for interface in re.findall(rf"{network_interface_reg_path}\\\d+", output):
        #get the adapter index
        adapter_index = int(interface.split("\\")[-1])
        interface_content = subprocess.check_output(f"reg QUERY {interface.strip()}").decode()
        if adapter_transport_name in interface_content:
            #change the MAC address using reg ADD command
            subprocess.check_output(f"reg add {interface} /v NetworkAddress /d {new_mac_address} /f").decode()
            break
    #return the index of the changed adapter's MAC address
    return adapter_index

# function to change mac address on linux

def change_mac_address_linux(iface, new_mac_address):
    try:
        #run ifconfig commands
        subprocess.check_output(f"ifconfig {iface} down", shell=True)
        subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}", shell=True)
        subprocess.check_output(f"ifconfig {iface} up", shell=True)
        new_mac_address = new_mac_address.upper()
        print(f"MAC address for {iface} changed to {new_mac_address}")
    except subprocess.CalledProcessError as e:
        print(f"Error changing MAC address for {iface}: {e}")

#function to get an adapter choice from user on windows
         
def get_user_adapter_choice_win(connected_adapters_mac):
    #print the available adapters
    for i, option in enumerate(connected_adapters_mac):
        print(f"{i}. {option[0]}")
    #prompt the user to choose a network adapter index
    try:
        choice = int(input("Choose interface:"))
        return connected_adapters_mac[choice]
    except:
        exit()

# MENU 
        
def display_menu():
    print("\nMENU:")
    print("1. Display current MAC Address")
    print("2. Change MAC Address")
    print("3. Reset MAC Address")
    print("4. Scan Network and List Connected Devices' MAC Addresses")
    print("5. Exit")
    choice = input("Enter choice: ")
    if (choice == "1"):
        #display mac address
        if (p == "win"):
            mac_addresses = get_mac_addresses_win()
            display_mac_addresses_win(mac_addresses)
        else:
            mac_addresses = get_mac_addresses_linux()
            display_mac_addresses_linux(mac_addresses)
        display_menu()
    elif (choice == "2"):
        #change mac address
        display_menu2()
    elif (choice == "3"):
        #reset
        loaded_mac_addresses = read_mac_addresses_from_file('mac_addresses.json')
        if loaded_mac_addresses:
            for iface, new_mac_address in loaded_mac_addresses[0].items():
                if p == "win":
                    change_mac_address_win(iface, new_mac_address)
                else:
                    change_mac_address_linux(iface, new_mac_address)
        else:
                print("No saved MAC Addresses found!")
        display_menu()
    elif (choice == "4"):
        scan_network()
    elif (choice == "5"):  
        exit()  

    else:
        print("Invalid choice!")
        display_menu()

#function to display the change mac address menu of program
def display_menu2():
    print("\n---MENU:\n1. Random\n2. From list of manufacturers\n3. Back\n")
    choice = input("Enter choice: ")
    if (choice == "1"):
        #random
        if (p == "win"):
            new_mac_address = get_random_mac_address_win()
            connected_adapters_mac = get_mac_addresses_win()
            old_mac_address, target_transport_name = get_user_adapter_choice_win(connected_adapters_mac)
            adapter_index = change_mac_address_win(target_transport_name, new_mac_address)
            disable_adapter(adapter_index)
            enable_adapter(adapter_index)
        else:
            mac_addresses = get_mac_addresses_linux()
            display_mac_addresses_linux(mac_addresses)
            iface = input("\nEnter interface: ")
            new_mac_address = get_random_mac_address_linux()
            change_mac_address_linux(iface, new_mac_address)
        display_menu()
    elif (choice == "2"):
        #list of manufacturers
        display_manufacturers()
        display_menu()
    elif (choice == "3"):
        #back
        display_menu()
    else:
        print("Invalid choice!")
        display_menu2()

#function to display the list of manufacturers
def display_manufacturers():
    print("\nMENU:")
    for index, company in enumerate(OUI.keys(), start=1):
            print(f"{index}. {company}")
    choice = input("\nEnter choice: ")
    company_name, mac_address = OUI_list[int(choice)-1]

    if (p == "win"):
        connected_adapters_mac = get_mac_addresses_win()
        old_mac_address, target_transport_name = get_user_adapter_choice_win(connected_adapters_mac)
        adapter_index = change_mac_address_win(target_transport_name, generate_random_mac_with_oui_win(mac_address.replace(":", "")))
        disable_adapter(adapter_index)
        enable_adapter(adapter_index)
    else:
        mac_addresses = get_mac_addresses_linux()
        display_mac_addresses_linux(mac_addresses)
        iface = input("\nEnter interface: ")
        print("")
        change_mac_address_linux(iface, generate_random_mac_with_oui_linux(mac_address.replace(":", "")))
    display_menu2()


# MAIN FUNCTION
    
if __name__ == "__main__":
    
    print("\nDeveloper Name: Syed Shayaan Hasnain Ahmad")

    print("Roll Number: 20I-0647")
    print("Section : B")
    print("BS Computer Science")
    print("Islamabad Campus")
    print("Ethical Hacking & Practices")

    print("\nSystem's current Date + Time: ", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("\nThe purpose of this tool is to interact with the NICs of a system, specifically to display, change, and reset the MAC addresses associated with those NICs")
    print("A Python tool that enables users to manipulate MAC addresses on both Windows and Linux operating systems.")


    #saving default mac addresses
    if os.path.exists("mac_addresses.json") == False:
        if (p == "win"):
            mac_addresses = get_mac_addresses_win()
        else:
            mac_addresses = get_mac_addresses_linux()
            
        save_mac_addresses_to_file(mac_addresses, 'mac_addresses.json')
    display_menu()
