#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import boto.manage.cmdshell
import time
import sys
from ssh_helper import run_remote_command 
from logger import create_log_file
from termcolor import colored
instance = None
instance_ip = ''
key = 'cfoskin_key.pem'
remote_host = "ec2-user@"
full_remote_host = ''
conn = ''
reservation=''
execute_all = 1

def options():
 choice = None
 while choice != '0':
     print("==================================================================")
     print('|  1: launch new instance and execute all services                |')
     print('|  2: launch new instance only                                    |')
     print('|  3: Install Nginx                                               |')
     print('|  4: Copy Nginx webserver script using SCP                       |')
     print('|  5: Change webserver script permissions                         |')
     print('|  6: Install Python 3 on instance                                |')
     print('|  7: Run script to check if Nginx is running and start if not    |')
     print('|  8: Stop Instance                                               |')
     print('|  9: Terminate Instance                                          |')
     print('|  0: EXIT  \n \n                                                 |')
     print("==================================================================")
     choice = input('which task to you want to perform? \n\n ')
     if choice == '1':launch_new_instance()
     if choice == '2':   
         global execute_all 
         execute_all = 0
         print(colored("  Please Note -- If You are Manually Running The Services Listed -- You Must Execute Sequentially From 3 ===>>> 7   ", 'red',attrs=['reverse', 'blink']))
         launch_new_instance()
     if choice == '3': install_nginx()
     if choice == '4': copy_webserver_script()
     if choice == '5': make_executable() 
     if choice == '6': install_python() 
     if choice == '7': run_webserver_script()
     if choice == '8': stop_instance()
     if choice == '9': terminate_instance()
     if choice == '0': sys.exit(0)    

def launch_new_instance():
 global conn
 conn = boto.ec2.connect_to_region("eu-west-1")
 global reservation
 reservation = conn.run_instances('ami-69b9941e', key_name = 'cfoskin_key', instance_type = 't2.micro', security_groups = ['witsshrdp'])
 global instance
 instance = reservation.instances[0]
 instance.add_tag('Name','GA_ColumFoskin')
 print('Instance Launching - Please wait for initialization... ')
 while instance.state != 'running':
     time.sleep(10)
     print(instance.update())
 else:
     print('Instance Launch Complete - Instance is Running \n')
     get_instance_info()
 if execute_all == 1:
     execute_all_services()
     
def execute_all_services():
 install_nginx()
 copy_webserver_script()
 make_executable()
 install_python() 
 run_webserver_script()

def wait_for_ssh_service():
 print('time sleep started while waiting for ssh to start')
 time.sleep(90)#must wait long enough to allow ssh service to start
 global instance_ip
 instance_ip = instance.ip_address
 global full_remote_host
 full_remote_host = remote_host + instance_ip

def install_nginx():
 if instance != None:
     wait_for_ssh_service()
     print('Proceedng with installation of nginx now using ssh...')
     cmd = " ssh -t -o StrictHostKeyChecking=no -i " + key + " " + full_remote_host + " 'sudo yum install -y nginx' "
     run_remote_command(instance, remote_host, key, cmd)
 else:
     print('\n You need to launch an instance first! \n')  
 
def copy_webserver_script():
 cmd = "scp -i " + key + " start_webserver.py " + full_remote_host +":."  
 run_remote_command(instance, remote_host, key, cmd)

def make_executable():
 cmd = "ssh -t -i " + key + " " + full_remote_host +" 'chmod 700 start_webserver.py'"
 run_remote_command(instance, remote_host, key, cmd)

def install_python():
 cmd = "ssh -t -i " + key + " " + full_remote_host + " 'sudo yum install -y python34'"
 run_remote_command(instance, remote_host, key, cmd)
  
def run_webserver_script():
 cmd = "ssh -t -i " + key + " " + full_remote_host +" python3 start_webserver.py"
 run_remote_command(instance, remote_host, key, cmd)
 
def get_instance_info():
 if instance != None:
     print('\nconnection to zone: ', conn)
     print('\nreservation id: ', reservation)
     print('\ninstance : %s' % instance.id,  ' state is: %s' % instance.state, ' ip address is: %s \n'% instance.ip_address)
 else:
     print('\nYou need to launch an instance first! \n\n')  
 
def stop_instance():
 if instance != None:
     if instance.state == 'running':
         reply = input('Are you sure that you want to stop the instance y/n? ')
         if reply == 'y':
             print('stopping instance now...')
             instance.stop()
             while instance.state != 'stopped':
                 time.sleep(5)
                 print(instance.update())
             else:
                 print('instance is stopped \n')
         else: 
             print('instance not stopped \n')
     else: 
         print('instance is not running! - cannot stop the instance \n')
 else:
     print('\nYou need to launch an instance first! \n\n')  

def terminate_instance():
 if instance != None:
     reply = input('Are you sure that you want to terminate the instance y/n? ')
     if reply == 'y':
         print('terminating instance now...')
         instance.terminate()
         while instance.state != 'terminated':
             time.sleep(5)
             print(instance.update())
         else:
             print('instance is stopped and terminated \n')
     else: 
         print('instance not terminated \n')
 else:
     print('\nYou need to launch an instance first! \n\n')  


def main(): 
 create_log_file()
 options()

if __name__ == '__main__':
  main()

  #var/log/ngnix/access.log