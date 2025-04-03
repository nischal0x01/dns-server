import socket
import glob
import json

port = 53  
ip = "127.0.0.1"  

# UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

# Loading zone files 
def load_zone():
    jsonZone = {}
    zonefiles = glob.glob('zones/*.zone')

    for zone in zonefiles:
        with open(zone) as zoneData:
            data = json.load(zoneData)
            zoneName = data["$origin"]
            jsonZone[zoneName] = data

    return jsonZone

zoneData = load_zone()


def getZone(domain):
    zone_name = ".".join(domain) + "."
    return zoneData.get(zone_name, {})


def getFlags(flags):
    byte1 = flags[0]
    QR = '1'  # Response

    OPCODE = format((byte1 >> 3) & 0x0F, '04b')  
    AA = '1'  
    TC = '0'  
    RD = '0'  

    byte2 = flags[1]
    RA = '0'  
    Z = '000'  
    RCODE = '0000'  

    return int(QR + OPCODE + AA + TC + RD, 2).to_bytes(1, byteorder='big') + \
           int(RA + Z + RCODE, 2).to_bytes(1, byteorder='big')


def getQuestionDomain(data):
    state = 0
    expectedLength = 0
    domainString = ''
    domainParts = []
    x = 0
    y = 0

    for byte in data:
        if state == 1:
            domainString += chr(byte)
            x += 1
            if x == expectedLength:
                domainParts.append(domainString)
                domainString = ''
                state = 0
                x = 0
            if byte == 0:
                break
        else:
            state = 1
            expectedLength = byte
        y += 1

    questionType = data[y:y + 2]
    return domainParts, questionType

# finding records
def getRecs(data):
    domain, questionType = getQuestionDomain(data)
    qt = ''

    if questionType == b'\x00\x01':  
        qt = 'A'

    zone = getZone(domain)
    return zone.get('records', {}).get(qt, []), qt, domain


def buildResponse(data):
    TransactionID = data[:2]
    Flags = getFlags(data[2:4])
    QDCOUNT = b'\x00\x01'  
    ANCOUNT = b'\x00\x01'  
    NSCOUNT = b'\x00\x00'
    ARCOUNT = b'\x00\x00'

    
    records, recordType, domainName = getRecs(data[12:])
    
    
    Question = data[12:data.find(b'\x00') + 5]

    
    Answer = b''
    for record in records:
        Answer += b'\xc0\x0c'  
        Answer += b'\x00\x01'
        Answer += b'\x00\x01'  
        Answer += b'\x00\x00\x00\x3c'  
        Answer += b'\x00\x04'  
        Answer += bytes(map(int, record.split('.')))  

    return TransactionID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT + Question + Answer

#  server loop
while True:
    data, addr = sock.recvfrom(512)
    response = buildResponse(data)
    sock.sendto(response, addr)
