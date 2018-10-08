import sys, time, threading
#====================  methods =====================================
'''
prints a small animaiton to chek that the program is still running
'''

def printAnimation():
    sys.stdout.write('0')
    time.sleep(0.5)
    sys.stdout.write('\b')
    time.sleep(0.25)
    sys.stdout.write('|')
    time.sleep(0.5)
    sys.stdout.write('\b')
    time.sleep(0.25)
''''
implementation of how to send a file to a server
'''''
def sendFile(filename,sock,*args):
    #t = threading.Thread(target= printAnimation)
    if args:
        filename = '{}/{}'.format(args[0],filename)
    with open (filename,'rb') as sfile:
        sys.stdout.write('sending data.')
        #t.start()
        while True:
            line = sfile.read(100)
            sock.send(line)
            print(line)
            #t.run()
            printAnimation()
            if not line: break              
        print()
    sys.stdout.write("data sent.")
    sfile.close()     


''''
implementation of how to get a file from a server 
'''''    
def getFile(filename,sock,*args):
    #t = threading.Thread(target = printAnimation)
    if args:
        filename = '{}/{}'.format(args[0],filename)
    with open(filename, 'wb') as rfile:
        sys.stdout.write("recieving data.")
        #t.start()
        while True:
            data = sock.recv(100)
            print(data)
            if not data: break
            rfile.write(data)
            #t.run()
            printAnimation()
        print()
    rfile.close()
    sys.stdout.write("data recieved")
