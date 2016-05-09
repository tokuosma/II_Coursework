import sys 
import socket 
import pieces
import struct
 
def main():
  portTCPin = 10000
  portTCPout = 10001
  portUDPc = 10002
  portUDPs = 10003

  # Create TCP sockets for client and server
  success = False  
  while not success: 
    try:
      if portTCPin > 10100:
        sys.exit()
      else:
        TCPin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        TCPin.bind(('', portTCPin))
        success = True
        print( "TCP socket for clients bound at port %d" % portTCPin)
    except OSError:
      TCPin.close()
      portTCPin += 1
  TCPout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Create UDP socket for client
  success = False
  while not success:
    try:
      if portUDPc > 10100:
        sys.exit()
      else:
        UDPc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPc.bind(('', portUDPc))
        success = True
    except OSError:
      UDPc.close()
      portUDPc += 1      

  # Create UDP socket for server
  success = False
  while not success:
    try:
      if portUDPs > 10100:
        sys.exit()
      else:
        UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPs.bind(('', portUDPs))
        success = True
    except OSError:
      UDPs.close()
      portUDPs += 1      



  # TCP handshake
  TCPin.listen(1)
  while True:
    connection, addr = TCPin.accept()
    print("Connection from %s:%d" % addr)
    data = connection.recv(4096).decode("utf-8")
    messageList = data.split(" ")
    clientport = int(messageList[1])
    print(messageList)
    ClientHelo = "{} {} {}".format(messageList[0], str(portUDPs), messageList[2])
    TCPout.connect(("ii.virtues.fi", 10000))
    TCPout.send(bytes(ClientHelo, "utf-8"))   
    ServerHelo = TCPout.recv(4096).decode("utf-8")
    messageList2 = ServerHelo.split(" ")
    serverport = int(messageList2[1])
    print(serverport)
    ServerHelo = "{} {}".format(messageList2[0], str(portUDPc))
    connection.send(bytes(ServerHelo, "utf-8"))
    break

  exit = False
  client = True
  count = 0
  
  while not exit:
    print("Count: %d" % count)

    if client == True:
      
      print("Listening to port %d" % portUDPc)
      received = UDPc.recvfrom(4096)[0]
      unpacked = struct.unpack("!??HH64s",received)
      if unpacked[3] == 0:
        client = False
      
      print("Sending to ii.virtues.fi:%d" % serverport)
      UDPs.sendto(received, ("ii.virtues.fi", serverport))
      count += 1
    elif client == False:
      print("Listening to port %d" % portUDPs)
      received = UDPs.recvfrom(4096)[0]
      unpacked = struct.unpack("!??HH64s",received)
      if unpacked[3] == 0:
        client = True
      UDPc.sendto(received, ("localhost", clientport))
      count += 1
      if unpacked[0]:
        break
  UDPs.close()       
  UDPc.close()
  TCPin.close()
  TCPout.close()

if __name__ == "__main__": 
  try: 
    main() 
  except KeyboardInterrupt: 
    sys.exit(1)

