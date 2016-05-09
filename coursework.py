import sys 
import struct
import socket 
import pieces
from questions import answer
from questions import QuestionNotFoundException
 
def main(): 
    if len(sys.argv) < 3: 
        sys.exit('usage: %s <hostname> <port number>' % sys.argv[0]) 
 
    try: 
        servAddr= sys.argv[1]
        servPort= int(sys.argv[2]) 

    except TypeError: 
        sys.exit("port must be an integer") 
 
    print("STOP!")
    print("Who would cross the bridge of death must answer me these questions n.")
    print("Creating TCP socket")
    TCPs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    print("Finding free port for UDP Socket")
    portUDP = 10001
    while True:
        try:
            UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            UDPs.bind(('', portUDP))
            print("UDP socket bound to port: %d" % portUDP)
            break
        except OSError:
            print("Port %d already taken. Trying next port" % portUDP)
            UDPs.close()
            portUDP = portUDP + 1
            continue

    print("Trying to form connection to %s at port %d" % (servAddr, servPort))
    TCPs.connect((servAddr, servPort))
    print("TCP connection formed to address %s at port %d" % (servAddr, servPort))
    helo = ("HELO %d MI\r\n" % portUDP)
    TCPs.send(bytes( helo, "utf-8"))
    received = TCPs.recvfrom(4096)
    data = received[0].decode("utf-8")
    destPort = int(data.split(" ")[1])
    destAddr = socket.gethostbyname(servAddr)

    print("Server address: %s Server UDP port: %d" % (destAddr, destPort))

    message = bytes("Ekki-ekki-ekki-ekki-PTANG.", "utf-8")
    dataOut = struct.pack("!??HH64s", False, True, len(message), 0, message)
    print("TCP handshake complete. Starting UDP transfer.")
    UDPs.sendto(dataOut, (servAddr, destPort))
    
    done = False
    while not done:
        received = UDPs.recvfrom(1024)
        dataIn = struct.unpack("!??HH64s", received[0])
        senderAddress = received[1]
        messageLength = len(dataIn[4].decode("utf-8").replace("\x00", ""))
        if dataIn[2] != messageLength:
            print( "Message lenght and header length do not match. Sending error message.")
            message = "Send again."
            error_message = struct.pack("!??HH64s", False, False, len(message), 0, bytes(message, "utf-8")) 
            UDPs.sendto(error_message, (servAddr, destPort))
            continue
        if messageLength == 0:
            print( "Empty message received. Sending error message.")
            message = "Send again."
            error_message = struct.pack("!??HH64s", False, False, len(message), 0, bytes(message, "utf-8")) 
            UDPs.sendto(error_message, (servAddr, destPort))
            continue
        if senderAddress[0] != destAddr or senderAddress[1] != destPort:
            print("Sender address does not match destination address. Sending error message.")
            message = "Send again."
            error_message = struct.pack("!??HH64s", False, False, len(message), 0, bytes(message, "utf-8")) 
            UDPs.sendto(error_message, (servAddr, destPort))
            continue

        stringList = []
        stringList.append(dataIn[4].decode("utf-8"))
        remaining = dataIn[3]
        done = dataIn[0]
        

        while not (remaining  == 0):
            received = UDPs.recvfrom(1024)
            dataIn = struct.unpack("!??HH64s", received[0])
            stringList.append(dataIn[4].decode("utf-8"))
            remaining = dataIn[3]
            done = dataIn[0]

        #question = dataIn[4].decode("utf-8").strip()
        question = pieces.parse_message(stringList)
        print(question)
        if not done:
            try:
                ans = answer(question)
                print(ans)
                ansPieces = pieces.pieces(ans)
                remaining_bytes = len(ansPieces) * 64
            except QuestionNotFoundException:
                print("Question not found. Sending error message.")
                message = "Send again."
                error_message = struct.pack("!??HH64s", False, False, len(message), 0, bytes(message, "utf-8")) 
                UDPs.sendto(error_message, (servAddr, destPort))
                continue
            else:
                for piece in ansPieces:
                    remaining_bytes -= 64
                    dataOut = struct.pack("!??HH64s", False, True, len(piece), remaining_bytes, bytes(piece, "utf-8"))
                    UDPs.sendto(dataOut, (servAddr, destPort))
                

    UDPs.close()
    TCPs.close()
     
if __name__ == '__main__': 
    try: 
        main() 
    except KeyboardInterrupt: 
        sys.exit(1) 
