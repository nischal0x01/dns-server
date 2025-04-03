import socket
port = 53
ip = "127.0.0.1" # loopback/local ip

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip,port))

def buildresponse(data):
    TransactionID = data[:2]
    pirnt(TransactionID)

while 1:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)

    sock.sendto(r, addr)
