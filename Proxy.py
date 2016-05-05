import sys 
import socket 
import pieces
import struct
 
def main():
  portTCPin = 10000
  portTCPout = 10001
  portUDP = 10002
  success = False  
  while not success: 
    try:
      if portTCPin > 10100:
        sys.exit()
      else:
        TCPin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        TCPin.bind(('', portTCPin))
        success = True
    except OSError:
      TCPin.close()
      portTCPin += 1
  success = False
  TCPout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  while not success:
    try:
      if portUDP > 10100:
        sys.exit()
      else:
          UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          UDPs.bind(('', portUDP))
          success = True
    except OSError:
      UDPs.close()
      portUDP += 1      
  TCPin.listen(1)
  while True:
    connection, addr = TCPin.accept()
    data = connection.recv(4096).decode("utf-8")
    messageList = data.split(" ")
    clientport = int(messageList[1])
    messageList[1] = str(portUDP)
    ClientHelo = "{} {}".format(messageList[0], messageList[1])
    TCPout.connect(("ii.virtues.fi", 10000))
    TCPout.send(bytes(ClientHelo, "utf-8"))   
    ServerHelo = TCPout.recv(4096).decode("utf-8")
    messageList2 = data.split(" ")
    serverport = int(messageList2[1])
    messageList2[1] = str(portUDP)
    ServerHelo = "{} {}".format(messageList2[0], messageList2[1])
    connection.send(bytes(ServerHelo, "utf-8"))
    TCPin.close()
    TCPout.close()
    break
  exit = False
  client = True
  while not exit:
    if client == True:
      received = UDPs.recvfrom(4096)
      client = False
      UDPs.sendto(received, serveraddr)
    elif client == False:
      received = UDPs.recvfrom(4096)
      client = True
      UDPs.sendto(received, clientaddr)
      break
  UDPs.close()       
if __name__ == '__main__': 
  try: 
    main() 
  except KeyboardInterrupt: 
    sys.exit() 
