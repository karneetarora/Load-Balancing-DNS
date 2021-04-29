import socket
from sys import argv
import argparse

parser = argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('port', type=int, help='This is the port ls will listen and connect to the client', action='store')
args = parser.parse_args(argv[1:])

#host = socket.gethostname()
print(f'[S]: Host is - {host}')

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[S]: Server socket created')

except socket.error as err:
    print(f"[S]: Couldn't create socket due to {err}")
    exit()
SERVER = ('', args.port)
ss.bind((SERVER))
ss.listen(1)

connection, address = ss.accept()

with connection:
    while True:
        data = connection.recv(512)
        data = data.decode('utf-8')
        #send query to hash function
        connection.sendall(data.encode('utf=8'))

ss.close()
exit()