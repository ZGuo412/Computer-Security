#Homework Header: 9
#Name: Ziyu Guo
#ECN Login: guo412
#DUE DATE: 3/28
#remove any previous rules or chains
sudo iptables -F
#for all outgoing packets, change their source IP address to my own.
sudo modprobe ip_nat_ftp
sudo iptables -t nat -A POSTROUTING -s 128.210.106.73 -o eth0 -j MASQUERADE
#block a list of specific ip addresses for all incoming connections
sudo iptables -A INPUT -s 199.95.207.0/24 -j DROP
#block my own computr from being pinged
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
#set up port-forwarding from an unused port of my choice to port 22.
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT #enable connections
sudo iptables -A FORWARD -p tcp --dport 22 -j ACCEPT
#allow ssh (port 22) to my own machine from my own machine
sudo iptables -A INPUT -s ecn.purdue.edu -p tcp --destination-port 22 -j ACCEPT
sudo iptables -A INPUT -j REJECT
#allows only a single IP address in the internet to my machine for the HTTP
sudo iptables -A INPUT -s 128.210.106.73 -p tcp --dport 22 -j ACCEPT
#permit Auth/Ident
sudo iptables -A INPUT -p tcp --dport 113 -j ACCEPT
