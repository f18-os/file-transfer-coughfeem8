#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
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
#====================== file  trasfer ===============================
# attempt to get file
print ('connection stablished to port: {0}'.format(serverPort))
request = input()
s.send(bytes(request,'utf-8'))
command, f =  re.split(' ', request)
if command == 'put':
   with open (f,'rb') as sfile:
       sys.stdout.write('sending data.')
       while True:
           line = sfile.read(100)
           s.send(line)
           sys.stdout.write('.')
           sys.stdout.write('\b')
           if not line:
               break              
       print()
   sys.stdout.write("data sent ")
   sfile.close()    
elif command == 'get':
   with open(f, 'wb') as rfile:
       sys.stdout.write("recieving data.")
       while True:
           data = s.recv(100)
           if not data: break
           rfile.write(data)
           sys.stdout.write('.')
           sys.stdout.write('\b')
       print()
   rfile.close()
   sys.stdout.write("data recieved")
else:
    print('that\'s  not a good format')
    sys.exit(1)
