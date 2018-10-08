

def fileMaker(name,size):
   with open(name+'.txt','w') as new_file:
       for i in range(size):
           new_file.write(str(i))
   new_file.close()

fileMaker('1megU',1000000)
fileMaker('server/1gigS',10000000)
