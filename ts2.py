import binascii
import socket
import argparse
from sys import argv

# First we use the argparse package to parse the arguments
parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port that ls will listen for.', action='store')
args = parser.parse_args(argv[1:])


class Hostname():
    def __init__(self, host, ip_address):
        self.host = host
        self.ip_address = ip_address


# Creating DNS table
table = []
def add_host(host, ip):
    host_name = Hostname(host, ip)
    table.append(host_name)


# checks to see if hostname is in the DNS Table
# if not, send dns request to cloudflare
def lookup(hostname):
    found = False
    for i in table:
        if i.host == hostname:
            found = True
            return f'{i.host} {i.ip_address}'
    if not found:
        # send udp request to cloudflare for IP address

        # add information sent from google to table, call add_host method
        return f'{host} - NS'


# Connect to LS
# Printing server info
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    localhost_ip = (socket.gethostbyname(host))
    print('[S]: TS2 Server socket created')
    print('[S]: The host is {}'.format(host))
    print('[S]: Server IP address is {}'.format(localhost_ip))
except socket.error as err:
    print("[S]: Couldn't create socket due to {}".format(err))
    exit()

# bind to address and listen for client
server_addr = (host, args.port)
ss.bind(server_addr)
ss.listen(1)

# accept a client
csockid, addr = ss.accept()
print()
print("[S]: Got a connection, client is at {}".format(addr))


# Close the server socket
ss.close()
exit()


