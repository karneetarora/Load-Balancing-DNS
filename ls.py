import socket
from sys import argv
import argparse

parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port ls will listen and connect to the client', action='store')
parser.add_argument('ts1host', type=str, help='This is the host of ts1', action='store')
parser.add_argument('ts1port', type=int, help='This is the port of ts1', action='store')
parser.add_argument('ts2host', type=str, help='This is the host of ts2', action='store')
parser.add_argument('ts2port', type=int, help='This is the port of ts2', action='store')
args = parser.parse_args(argv[1:])

# host = socket.gethostname()
# print(f'[S]: Host is - {host}')

# create server socket to communicate with client
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print("[S]: Couldn't create socket due to {}".format(err))
    exit()

# choose a port for the server
server_addr = (socket.gethostname(), args.port)
ss.bind(server_addr)
ss.listen(1)

# print server information
host = socket.gethostname()
print("[S]: The host is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP: {}".format(localhost_ip))

# accept a client
csockid, addr = ss.accept()
print("[S]: Got a connection, client is at {}".format(addr))

connection, address = ss.accept()

while True:
    clientData = csockid.recv(512)
    if not clientData:
        break
    clientData = clientData.decode('utf-8')
    # send query to hash function
    connection.sendall(clientData.encode('utf=8'))

# Close the server socket
ss.close()
exit()