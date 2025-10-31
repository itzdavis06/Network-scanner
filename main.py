import nmap

import re

#to recognize ipv4 
ip_pattern=re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

#to recognize port
port_pattern=re.compile(r"([0-9]+)-([0-9]+)$")
port_min=0
port_max=65535


openPorts=[]

if __name__=='__main__':
    while True:
        ipEntered = input('Enter valid ip address to scan: ')
        if ip_pattern.search(ipEntered):
            print(f'{ipEntered} is a valid ip address')
            break

    
    while True:
        portEntered = input('Enter port range (min-max eg 54-980) : ')
        validPort = port_pattern.search(portEntered.replace(' ', ''))
        if validPort:
            port_min = int(validPort.group(1))
            port_max = int(validPort.group(2))
            break


    nm=nmap.PortScanner()

    for port in range(port_min,port_max + 1):
        try:
            result=nm.scan(ipEntered,str(port))
           # print(result)

            portStatus=(result['scan'][ipEntered]['tcp'][port]['state'])
            print(f'port {port} is {portStatus}')
        except Exception as e:
            print(f'Cannot scan port {port}: {e}')


   