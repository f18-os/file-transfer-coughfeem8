#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params
import params, re, socket, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


#====================  methods =====================================
def printAnimation():
    sys.stdout.write('0')
    sys.stdout.write('\b')
    sys.stdout.write('|')
    sys.stdout.write('\b')

def sendFile(filename, socket):
    with open ('server/'+filename,'rb') as sfile:
        sys.stdout.write('sending data.')
        while True:
            line = sfile.read(100)
            socket.send(line)
            printAnimation()
            if not line: break              
        print()
    sys.stdout.write("data sent. ")
    sfile.close()     
    
def getFile(filename,socket):
    with open('server/'+filename, 'wb') as rfile:
        sys.stdout.write("recieving data.")
        while True:
            data = socket.recv(100)
            if not data: break
            rfile.write(data)
            printAnimation()
        print()
    rfile.close()
    sys.stdout.write("data recieved")

# ================== file transfer ==================================
while True:
    sock, addr = lsock.accept()
    
    print("connection rec'd from", addr)
    request = sock.recv(100)
    request = request.decode('utf-8')
    print(request)
    command , f = re.split(' ', request)
    #server sends a file
    if command == 'get':
        sendFile(f,sock)
    #server  recieves a file    
    elif command == 'put':
        getFile(f,sock)
    else:
        print('wrong format, buddy. ')
        continue

    
