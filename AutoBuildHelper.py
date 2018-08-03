import os
import subprocess
import datetime
def RunCommand(command):
      pipe = os.popen(command)
      info = pipe.read()
      print(info) 

def RunCommandWithLog(command, print_msg=True):
     pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
     state = True
     for line in iter(pipe.stdout.readline, b''):
        if print_msg:
            line = line.rstrip().decode('utf8')
            line.strip('\n')
            print(">>>", line)
        if line == 'BUILD FAILED':
           state = False
     return state      

def ReNameFolderName(file_name, must_rename=True):
      nowTime=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

      try:
       os.rename(file_name, file_name + '_' + nowTime) 
      except OSError:
       print(file_name + ' Can not be renamed')
       if  must_rename:
            return False

      return True 
      
     
      
      
      

     
          

