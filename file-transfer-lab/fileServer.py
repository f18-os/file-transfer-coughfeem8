#! /usr/bin/env python3
import sys, re, socket
sys.path.append("../lib")       # for params
import params

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

sock, addr = lsock.accept()
print("connection rec'd from", addr)

# ================== file transfer ==================================
request = sock.recv(100)
request = request.decode('utf-8')
print(request)
command , f = re.split(' ', request)
#server sends a file
if command == 'get':
    with open('server/'+f , 'rb') as send_file:
          sys.stdout.write("sending data.")
          while True:
              data = send_file.read(100)
              if not data:  break
              sock.send(data)
              sys.stdout.write('.')
              sys.stdout.write('\b')
          print()
    sys.stdout.write("data sent")
    send_file.close()
#server  recieves a file    
elif command == 'put':
    with open('server/'+f, 'wb') as rec_file:
        sys.stdout.write('recviving data.')
        while True:
            data = sock.recv(100)
            if not data:
                print('ERROR WHILE RECIEVING')
                break
            rec_file.write(data)
            sys.stdout.write('.')
            sys.stdout.write('\b')
        print()
    sys.stdout.write("data recieved")
    rec_file.close()
else:
    print('wrong format, buddy. ')
    sys.exit(1)

    
