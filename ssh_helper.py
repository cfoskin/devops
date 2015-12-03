#colum foskin 
#!/usr/bin/python3
#python program to assist with remote ssh commands. 

import subprocess
from logger import log_to_file 
from termcolor import colored
import sys

#takes in a command from run_web_server.py and runs it while dealing with the error or succes scenarios.
def run_remote_command(instance, cmd):
 if instance != None:
     (status,output) = subprocess.getstatusoutput(cmd)
     if status >0:
         print("status: %d \n" % status)
         handle_ssh_errors(output, status, cmd)
         return bool(0)#this is used so I can loop to install nginx until this is successful (in case ssh has not started and it fails).
     else:
         print("status:", status)
         handle_ssh_success(cmd)
         print(output)
 else:
     print('\n You need to launch an instance first! \n')  

#this function hanndles the errors resulting from an unsuccessful remote ssh call executed above.
#it prints a valid error message for the user and logs the status code and output to the file created in logger.py.
def handle_ssh_errors(status, output, cmd):
 if "install -y nginx" in cmd:
     print(colored('Failure installing nginx \n', 'red',attrs=['reverse', 'blink']))
     log_to_file(status, output)
 elif "scp" in cmd:
     print(colored('Failure copying script using SCP \n Please Check the Command and Restart Program to Try Process Again\n', 'red',attrs=['reverse', 'blink']))
     log_to_file(status, output)
     sys.exit(1)
 elif "chmod 700" in cmd:
     print(colored('Failure changing permissions on webserver script \n Please Check the Command and Restart Program To Try Process Again\n', 'red',attrs=['reverse', 'blink']))
     log_to_file(status, output) 
     sys.exit(1)
 elif "-y python34" in cmd:
     print(colored('Failure installing python\n', 'red',attrs=['reverse', 'blink']))
     log_to_file(status, output)
     sys.exit(1)
 elif "python3 start_webserver.py" in cmd:
     print(colored("Failure starting webserver \n Please Check the Command and Restart Program To Try Process Again \n", 'red',attrs=['reverse', 'blink']))
     log_to_file(status, output)
     sys.exit(1)
 else:
     print('Error')

 #this function prints the success mesaage based on the given command
def handle_ssh_success(cmd):
 if "install -y nginx" in cmd:
     print('nginx installed!\n')
 elif "scp" in cmd:
     print('SCP successful! \n')
 elif "chmod 700" in cmd:
     print('permissions changed!\n')
 elif "-y python34" in cmd:
     print('Python 3 installed!\n')
 else:
     print("success \n\n")
 