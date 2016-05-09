Introduction to the Internet 2016
Coursework

Group name: Internetin ihmeet

Group members:
Janne Eskola
Teemu Ikävalko
Toni Kuosmanen
Tapio Kursula

Description:
Program written for Python 3. Main program (coursework.py) implements multipart messages and integrity
checking. Proxy server implemented as a separate program (Proxy.py). 

Instructions:
1) Start up the proxy server (Proxy.py). Proxy will start listening to client
requests on first available port in range 10000 - 10100. The port chosen is
printed to the console.

2) Start the main program with the commands:
 $: python3 coursework.py <localhost> <proxy client port>

Alternatively if you're not running the proxy you can connect directly to the
server by substituting localhost with the server name.

3) Program will print out the questions received from the server and the
answer given. If the integrity check fails for some message program will print
out what caused the check to fail. 
