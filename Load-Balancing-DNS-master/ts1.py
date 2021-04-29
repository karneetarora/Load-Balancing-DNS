import socket
import argparse
from sys import argv

# First we use the argparse package to parse the arguments
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
    print("[S]: Socket created")
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

# starting here is the code from project 3
# This function sends a message to the UDP server
# Function taken from resource: "https://routley.io/posts/hand-writing-dns-messages/"
def send_udp_message(message, address, port):
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


# This function returns a pretty version of a hex string
# Function taken from resource: https://routley.io/posts/hand-writing-dns-messages/
def format_hex(hex):
    octets = [hex[i:i + 2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i + 2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)


# This function converts letters into hex
def toHex(s, lin):
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        lin.append(hv)
    return lin


# This function concatenates each element in the list together
def concatenateList(list):
    result = ""
    for element in list:
        result += str(element)
        result += ' '
    return result


# This function makes the final hexadecimal DNS query
def domainToHex(domainName):
    firstPart = "AA AA 01 00 00 01 00 00 00 00 00 00 "
    lastPart = "00 01 00 01"

    domainName_list = domainName.split(".")
    stringcount = len(domainName_list)
    ListofSizesOfParts = []

    for i in range(stringcount):
        if len(domainName_list[i]) < 10:
            ListofSizesOfParts.append("%02d" % len(domainName_list[i]))
            toHex(domainName_list[i], ListofSizesOfParts)
        elif len(domainName_list[i]) >= 10:
            ListofSizesOfParts.append(len(domainName_list[i]))
            toHex(domainName_list[i], ListofSizesOfParts)
    ListofSizesOfParts.append('00')

    finalResult = firstPart + concatenateList(ListofSizesOfParts) + lastPart
    return finalResult


while True:
    clientData = csockid.recv(512)
    if not clientData:
        break
    clientData = clientData.decode('utf-8')

    DNSquery = domainToHex(clientData)

    response = send_udp_message(DNSquery, "8.8.8.8", 53)
    finResponse = format_hex(response)

    finResponseList = finResponse.split()
    res = finResponseList[-4:]

    final = []
    for i in range(len(res)):
        final.append(int(res[i], 16))

    finalIP = ""
    for element in final:
        finalIP += str(element)
        finalIP += '.'
    finalIP = finalIP[:-1]

    csockid.send(finalIP.encode('utf-8'))

# Close the server socket
ss.close()
exit()


