import socket
import argparse
from sys import argv

parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port to ts1 will listen for.', action='store')
args = parser.parse_args(argv[1:])

class Hostname():
    def __init__(self, host, ip_address):
        self.host = host
        self.ip_address = ip_address


table = []
def add_host(host, ip):
    host_name = Hostname(host, ip)
    table.append(host_name)


def lookup(hostname):
    found = False
    for i in table:
        if i.host == hostname:
            found = True
            return f'{i.host} {i.ip_address}'
    if not found:
        #send udp request to google for IP address

        #add information sent from google to table, call add_host method
        return f'{host} - NS'


try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    localhost_ip = (socket.gethostbyname(host))
    print('[S]: Server socket created')
    print('[S]: The host is {}'.format(host))
    print('[S]: Server IP address is {}'.format(localhost_ip))
except socket.error as err:
    print(f"[S]: Couldn't create socket due to {err}")
    exit()

# choose a port
SERVER = ('', args.port)
ss.bind(SERVER)
ss.listen(1)

# accept a client
connection, address = ss.accept()

with connection:
    while True:
        data = connection.recv(512)
        data = data.decode('utf-8')
        data = lookup(data)
        connection.sendall(data.encode('utf=8'))

ss.close()
exit()
