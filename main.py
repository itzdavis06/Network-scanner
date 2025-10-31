import nmap
import re

# to recognize ipv4 
ip_pattern = re.compile(r"^((?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}"
                        r"([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$")

# to recognize port
port_pattern = re.compile(r"([0-9]+)-([0-9]+)$")

subnet_pattern = re.compile(r"^(?:[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]\.){3}[0]\/0?[0-9]|[1-2][0-9]|3[0-2]$")
port_min = 0
port_max = 65535

if __name__ == '__main__':
    print('***PRESS P for port scan***')
    print('***PRESS PI for ping scan***')

    Choice = input('Enter your choice : ').upper()

    if Choice == 'P':
        while True:
            ipEntered = input('Enter valid ip address to scan within 255.255.255.255 : ')
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

        nm = nmap.PortScanner()

        try:
            result = nm.scan(ipEntered, f'{port_min}-{port_max}')
            # for port in result['scan'][ipEntered]['tcp']:
            #     portStatus = (result['scan'][ipEntered]['tcp'][port]['state'])
            #     print(f'port {port} is {portStatus}')
            for host in nm.all_hosts():
                print(f'Host: {host} {nm[host].hostname()}')
                print(f'State: {nm[host].state()}')

                if 'tcp' in nm[host]:
                    for port in sorted(nm[host]['tcp'].keys()):
                        state = nm[host]['tcp'][port]['state']
                        service = nm[host]['tcp'][port].get('name', 'unknown')
                        print(f'         Port {port}: {state} {service}')

        except Exception as e:
            print(f'cannot scan port: {e}')

    elif Choice == 'PI':
        while True:
            SubEntered = input('Enter valid ip address with subnet add eg x.y.z.0/24 : ')
            if subnet_pattern.search(SubEntered):
                print(f'{SubEntered} is a valid subnet')
                break

        nm = nmap.PortScanner()

        res = nm.scan(SubEntered, arguments='-sn')
        hosts = nm.all_hosts()
        print('discovered hosts')
        for h in hosts:
            print(h, nm[h].hostname(), nm[h].state())
