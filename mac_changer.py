#!usr/share/bin/env python3

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface", help = "Enter the interface to change mac address")
    parser.add_option("-m", "--mac", dest = "new_mac", help = "MAC address to change to ")
    (options,arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+]Specify the Interface")
    if not options.new_mac:
        parser.error("[+]Specify the MAC Address")
    return options

def change_mac(interface,new_mac):
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig",interface,"up"])
    subprocess.call(["ifconfig",interface])

def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        print(mac_address_search_result.group(0))
    else:
        print("[-] Could not read mac address")

options = get_arguments()

current_mac = get_mac(options.interface)
print("Current Mac = " + str(current_mac))

change_mac(options.interface,options.new_mac)
new_mac = get_mac(options.interface)
if current_mac == new_mac:
     print("[+]MAC address was successfully changed")
else:
     print("[-]The Operation was unsuccessful")