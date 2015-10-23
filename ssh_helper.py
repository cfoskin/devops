#colum foskin 20062042
#!/usr/bin/python3
import subprocess
from logger import * 
from termcolor import colored

def run_remote_command(instance, remote_host, key, cmd):
 if instance != None:
     (status,output) = subprocess.getstatusoutput(cmd)
     if status >0:
         print("status: %d \n" % status)
         handle_ssh_errors(output, status, cmd)
     else:
         print("status:", status)
         handle_ssh_success(cmd)
         print(output)
 else:
     print('\n You need to launch an instance first! \n')  


def handle_ssh_errors(status, output, cmd):
 if "install -y nginx" in cmd:
     print('Failure installing nginx \n')
     log_to_file(status, output)
 elif "scp" in cmd:
     print('Failure copying script using SCP\n')
     log_to_file(status, output)
 elif "chmod 700" in cmd:
     print('Failure changing permissions on webserver script\n')
     log_to_file(status, output) 
 elif "-y python34" in cmd:
     print('Failure installing python\n')
     log_to_file(status, output)
 elif "python3 start_webserver.py" in cmd:
     print("Failure starting webserver\n")
     log_to_file(status, output)
 
def handle_ssh_success(cmd):
 if "install -y nginx" in cmd:
     print('nginx installed!\n')
 elif "scp" in cmd:
     print('SCP successful! \n')
 elif "chmod 700" in cmd:
     print('permissions changed!\n')
 elif "-y python34" in cmd:
     print('Python 3 installed!\n')
 elif "python3 start_webserver.py" in cmd:
     print("webserver started!\n")
 