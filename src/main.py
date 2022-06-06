import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # Internet, UDP

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1623) # reuse already used port address 1600
                                                           # deblock if former programm run got crashed

s.setblocking(0)                 # setting to non-blocking socket mode -> socket.SOCK_NONBLOCK not supported by Windows


s.bind(('localhost', 1623))      # Socket stays open + keeps used Portnummer... if not properly closed at the end
                                 # double parenthesis since 1 parameter (== union) expected

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

LICHT = False

while True:
    # Abbruch der Schleife
    
    try:
        msg, addr = s.recvfrom(1024)  
        # Normally blocks here if no Date reception -> Keyboard press not detected
        # Thus: placing socket in non-blocking mode required (see above)
        # generates "BlockingIOError" if Data couldn't be read at once -> Handling necessary
        # 1024 == amount of bytes to read at maximum
        print("Got message from %s: %s" % (addr, msg))
        S_01 = int(msg)
        LICHT = S_01
    except socket.error as e:   # supress BlockingIOError from non-blocking socket access if no Data received
        #print ("Error creating socket: %s" % e)
        pass    
   
    sock.sendto(str.encode(str(LICHT)), ('localhost', 1711))
s.close()    # close socket
print ("Socket closed")
