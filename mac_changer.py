#!usr/share/bin/env python3


#Three libraries are used implement the script
import subprocess
import optparse
import re



#This function takes arguments (as evident from the function's name)and returns them. 
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


#This block uses the subprocess library to cahnge the MAC address according to the user. 
#subprocess library is used to implement terminal command using python

def change_mac(interface,new_mac):
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig",interface,"up"])
    subprocess.call(["ifconfig",interface])
    

#This takes the mac address provided by user and checks if its valid and also the desired output was achieved or not     

def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
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
