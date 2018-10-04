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

''''
implementation of how to send a file to a client 
'''''
def sendFile(filename, so):
    with open ('server/'+filename,'rb') as sfile:
        sys.stdout.write('sending data.')
        while True:
            line = sfile.read(100)
            so.send(line)
            printAnimation()
            if not line: break              
        print()
    sys.stdout.write("data sent. ")
    sfile.close()     


''''
implementation of how to recieve a file from  a client
'''''    
def getFile(filename,so):
    with open('server/'+filename, 'wb') as rfile:
        sys.stdout.write("recieving data.")
        while True:
            data = so.recv(100)
            if not data: break
            rfile.write(data)
            printAnimation()
        print()
    rfile.close()
    sys.stdout.write("data recieved")

# ================== file transfer ==================================
while True:
    sock, addr = lsock.accept()
    
    if not os.fork():
        print("connection rec'd from", addr)
        request = sock.recv(100)
        request = request.decode('utf-8')
        print(request)
        command , f = re.split(' ', request)

        #server sends a file
        if command == 'get':
            if (not os.path.isfile(f)) or os.path.getsize(f) == 0 :
                print('file: {0} doesn\'t exits or is too small.'.format(f))
                continue
            sendFile(f,sock)

        #server  recieves a file    
        elif command == 'put':
            if os.path.isfile(f):
                 print('you already have {0}.'.format(f))
                 continue
            getFile(f,sock)
        else:
            print('wrong format, buddy. ')
            continue


