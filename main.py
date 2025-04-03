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

        AA='1'
        TC='0'
        RD='0'
        RA='0'
        Z='000'
        RCODE = '0000'
        return int(QR+OPCODE+AA+TC+RD,2).to_bytes(1,byteorder='big')+(RA+Z+RCODE).to_bytes(1,byteorder='big')





def getQuestionDomain(data):
    state=0
    expectedLength=0
    domainString=''
    domainParts = []
    x=0

    for byte in data:
        if state == 1:
            domainString+=chr(byte)
            if x== expectedLength:
                domainParts.append(domainString)
                domainString=''
        
        else:
            state=1
            expectedLength= byte
    print(domainString)

def buildresponse(data):

    #Transaction ID
    TransactionID = data[:2]
    TID=""

    for byte in TransactionID:
        TID+= hex(byte[2:])
    # flags
    Flags = getFlags(data[2:4])
    print(Flags)
    
    #Question Count
    QDCOUNT = b'\x00\x01'

    #Answer Count
    getQuestionDomain(data[12:])


while 1:
    data, addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r, addr)
