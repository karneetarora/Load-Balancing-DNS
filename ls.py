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

# stuff as CLIENT for connecting to top level servers--------------------------------------------
# create client socket to communicate with ts1
try:
    server_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Client socket for TS1 created")
except socket.error as err:
    print("[S]: Couldn't create socket due to {}".format(err))
    exit()

# create client socket to communicate with ts2
try:
    server_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Client socket 2 for TS2 created")
except socket.error as err:
    print('socket 2 open error: {} \n'.format(err))
    exit()

# connect to ts1 host
server_addr1 = (args.ts1host, args.ts1port)
server_sock1.connect(server_addr1)

# connect to ts2 host
server_addr2 = (args.ts2host, args.ts2port)
server_sock2.connect(server_addr2)


# print server information
host = socket.gethostname()
print("[S]: The host is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP: {}".format(localhost_ip))


# stuff as SERVER for connecting to client-----------------------------------------------
# Connect to client
# Printing server info
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    localhost_ip = (socket.gethostbyname(host))
    print()
    print('[S]: LS Server socket created')
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
print("[S]: Got a connection, client is at {}".format(addr))

with csockid:
    while True:
        clientData = csockid.recv(512)
        if not clientData:
            break
        clientData = clientData.decode('utf-8')

        tsServer = hash(clientData[4]) % 2
        # either send to server_sock1 or server_sock2
        if tsServer == 0:
            server_sock1.sendall(clientData.encode('utf-8'))
            newClientData = server_sock1.recv(512)
        else:
            server_sock2.sendall(clientData.encode('utf-8'))
            newClientData = server_sock2.recv(512)

        newClientData = newClientData.decode('utf-8')
        csockid.sendall(newClientData.encode('utf-8'))

# Close the server socket
ss.close()
exit()

