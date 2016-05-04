import sys 
import struct
import socket 
from questions import answer
 
def main(): 
    if len(sys.argv) < 3: 
        sys.exit('usage: %s <hostname> <port number>' % sys.argv[0]) 
 
    try: 
        servAddr= sys.argv[1]
        servPort= int(sys.argv[2]) 
    except TypeError: 
        sys.exit("port must be an integer") 
 
    port = 10000
    TCPs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    TCPs.bind(('', port)) 

    UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    portUDP = 10001
    UDPs.bind(('', portUDP))

    TCPs.connect((servAddr, servPort))
    TCPs.send(bytes("HELO 10001\r\n", "utf-8"))
    data = TCPs.recv(4096).decode("utf-8")
    destPort = int(data.partition(" ")[2].strip())

    eom = False
    ack = True
    message = bytes("Ekki-ekki-ekki-ekki-PTANG.", "utf-8")
    length = len(message)
    remaining = 0
    dataOut = struct.pack("!??HH64s", eom, ack, length, remaining, message)
    UDPs.sendto(dataOut, (servAddr, destPort))
    
    done = False
    while not done:
        received = UDPs.recvfrom(1024)
        dataIn = struct.unpack("!??HH64s", received[0])
        question = dataIn[4].decode("utf-8").strip()
        done = dataIn[0]
        print(question)
        if not done:
            ans = answer(question)
            print(ans)
            dataOut = struct.pack("!??HH64s", eom, ack, len(ans), 0, bytes(ans, "utf-8"))
            UDPs.sendto(dataOut, (servAddr, destPort))

    UDPs.close()
    TCPs.close()
     
if __name__ == '__main__': 
    try: 
        main() 
    except KeyboardInterrupt: 
        sys.exit(1) 