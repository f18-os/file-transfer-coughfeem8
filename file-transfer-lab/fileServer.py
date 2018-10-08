#! /usr/bin/env python3
import sys
sys.path.append("../lib")       # for params
sys.path.append('../framed-echo')
import params, re, socket, os
from fileSock import sendFile, getFile #for files 
from framedSock import framedSend, framedReceive  # for commands

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

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


# ================== file transfer ==================================
while True:
    sock, addr = lsock.accept()
    
    if not os.fork():
        print("CONNECTION FROM CHILD REC'D FROM ", addr)
        while True: #just keep connected to the client until it exits 
            request = framedReceive(sock,debug)
            if request:
                request = request.decode('utf-8')
                request = request.rstrip()
            else:
                print( 'SERVER DISCONNECTED FROM {}.'.format(addr))
                break

            #get the client input parsed
            data =  re.split(' ', request)
            try:
                command, f = data
            except:
                print ('WRONG FORMAT RECIEVED')
                continue

            #server sends a file
            if command == 'get':
                if (not os.path.isfile('server/'+f)) or os.stat('server/'+f) <= 0:
                    print('FILE: <{}> NOT IN SERVER/TOO SMALLl.'
                          .format(f))
                    continue
                sendFile(f,sock,'server')
            #server  recieves a file    
            elif command == 'put':
                if os.path.isfile('server/'+f):
                    print('<{}> ALREADY IN SERVER.'.format(f))
                    continue
                getFile(f,sock,'server')
            else:   
                print('WRONG INSTRUCTON RECIEVED.')
                continue
