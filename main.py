import socket
port = 53
ip = "127.0.0.1" # loopback/local ip

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip,port))

def getFlags(flags):
    byte1= bytes(flags[:1])
    byte2= bytes(flags[1:2])
    rflags= ''
    QR='1'

    OPCODE=""
    for bit in range(1,5):
        OPCODE+=str(ord(byte1)&(1<<bit))





def buildresponse(data):

#Transaction ID
    TransactionID = data[:2]
    TID=""

    for byte in TransactionID:
        TID+= hex(byte[2:])
# flags
Flags = getflags(data[2:4])

while 1:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r, addr)
