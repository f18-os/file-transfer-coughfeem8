#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params



switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),#  to proxy
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server= paramMap["server"]
usage = paramMap["usage"]
debug = paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort
                              , socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" %
              (af,socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

#====================  methods =====================================
'''
prints a small animaiton to chek that the program is still running
'''
def printAnimation():
    sys.stdout.write('0')
    sys.stdout.write('\b')
    sys.stdout.write('|')
    sys.stdout.write('\b')

''''
implementation of how to send a file to a server
'''''
def sendFile(filename):
    with open (filename,'rb') as sfile:
        sys.stdout.write('sending data.')
        while True:
            line = sfile.read(100)
            s.send(line)
            printAnimation()
            if not line: break              
        print()
    sys.stdout.write("data sent. ")
    sfile.close()     

''''
implementation of how to get a file from a server 
'''''    
def getFile(filename):
    with open(filename, 'wb') as rfile:
        sys.stdout.write("recieving data.")
        while True:
            data = s.recv(100)
            if not data: break
            rfile.write(data)
            printAnimation()
        print()
    rfile.close()
    sys.stdout.write("data recieved")

#====================== file  trasfer ===============================

while True:
    request = input()
    s.send(bytes(request,'utf-8'))

    #check if client uses direct conection to the server
    command =  re.split(' ', request)
    f= command[1]
    try:
        direct = command[2]
    except:
        direct = False
    command = command[0]

    
    #connect to the proxy automatically
    if direct:
        serverPort = 50001
        print ('connection stablished to port: {0}'.format(serverPort))
    elif command == 'put':
        if (not os.path.isfile(f)) or  os.path.getsize(f) == 0:
            print('file: {0} doesn\'t exits or is too small.'.format(f))
            continue
        sendFile(f)  
    elif command == 'get':
        if os.path.isfile(f):
            print('you already have {0}.'.format(f))
            continue
        getFile(f)
    #end command disconecting
    elif request == 'exit':
        print('disconecting')
        sys.exit(1)        
    else: #zero size command
        print('that\'s  not a good format')

