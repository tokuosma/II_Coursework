import sys 
import socket 
import pieces
 
def main():
  portTCPin = 10002
  portTCPout = 10004
  success = False  
  while not success: 
    try:
      TCPin = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      TCPin.bind(('', portTCPin))
      TCPout = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
      TCPout.bind(('', portTCPout))
      success = True
    except OSError:
      TCPin.close()
      port += 1    
  success = False
  UDPs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  portUDP = 10003
  UDPs.bind(('', portUDP))   
  TCPin.listen(1)
  while True:
    connection, addr = TCPin.accept()
    data = connection.recv(4096).decode("utf-8")
    messageList = data.split(" ")
    clientport = messageList[1]
    messageList[1] = str(portUDP)
    dataout = "{} {}".format(messageList[0], messageList[1])
    TCPout.connect(("ii.virtues.fi", 10000))
    TCPout.send(bytes(dataout, "utf-8"))    
    break
  #while True:
    #connection, addr = TCPin.accept()
    #data = connection.recv(4096).decode("utf-8")
    #messageList = data.split(" ")
    #serverport = messageList[1]
    #messageList[1] = str(portUDP)
    #print(messageList)
    #dataout = "{} {}".format(messageList[0], messageList[1])
    #print(dataout)
    #TCPout.connect(("localhost", 10002))
    #TCPout.send(bytes(dataout, "utf-8"))
    #break 
  #UDPs.listen(1)
  print("loppusuora")
  while True:
    (UDPs, addr) = UDPs.accept()
    msg = UDPs.recv(4096)
    print(msg)

  while True:
    UDPs.close()
    break
  TCPin.close()
  
if __name__ == '__main__': 
  try: 
    main() 
  except KeyboardInterrupt: 
    sys.exit() 
