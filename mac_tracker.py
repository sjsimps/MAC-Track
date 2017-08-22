
import subprocess
import socket
import fcntl
import struct
from datetime import datetime
import time
import sys

class MacTracker:
    def __init__(self, interface):
        self.interface = interface
        self.ip_addr = self.get_ip_address(self.interface)

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15])
        )[20:24])

    def get_connected_devices(self):
        get_addrs = "sudo nmap -sP {}/24".format(self.ip_addr)
        find_mac = "grep -oh \"[0-9,A-F][0-9,A-F]:[0-9,A-F][0-9,A-F]:"\
                    "[0-9,A-F][0-9,A-F]:[0-9,A-F][0-9,A-F]:[0-9,A-F]"\
                    "[0-9,A-F]:[0-9,A-F][0-9,A-F]\""
        get_mac_addrs = "{} | {}".format(get_addrs, find_mac)

        p = subprocess.Popen([get_mac_addrs, ""], stdout=subprocess.PIPE, shell=True)
        output = p.communicate()
        self.mac_addrs = filter(None, output[0].split('\n'))
        return self.mac_addrs

    def log_connected_devices(self):
        self.date = time.strftime("%d_%m_%Y")
        logfile = "Devices_{}".format(self.date)
        f = open(logfile,'a')

        now = datetime.now()
        seconds_since_midnight = (now - now.replace(hour=0,
                                                    minute=0,
                                                    second=0,
                                                    microsecond=0)).total_seconds()

        for mac in self.mac_addrs:
            f.write("{},{},green\n".format(seconds_since_midnight,
                                           mac))

###############################################################################

interface = "wlan0"
poll_rate = 60 # seconds

def print_help():
    print "\nUsage: python mac_tracker.py [i=interface p=poll_rate]\n"

count = 0
for a in sys.argv:
    if count > 0:
        command = a.split('=')
        if len(command) != 2:
            print_help()
            exit()
        if command[0] == 'i':
            interface = command[1]
        elif command[0] == 'p':
            poll_rate = int(command[1])
        else:
            print_help()
            exit()
    count += 1

tracker = MacTracker(interface)

while True:
    poll = datetime.now()
    print tracker.get_connected_devices()
    tracker.log_connected_devices()
    while (datetime.now() - poll).total_seconds() < poll_rate :
        time.sleep(1)
