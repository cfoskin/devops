#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import boto.manage.cmdshell
import time
import sys
from logger import * 
from ssh_helper import run_remote_command 
instance = None
instance_ip = ''
key = 'cfoskin_key.pem'
remote_host = "ec2-user@"
full_remote_host = ''
conn = ''
reservation=''
execute_all = 1

def choose_task(choice):
 if choice == 1:   launch_new_instance()
 if choice == 2:   
     global execute_all 
     execute_all = 0
     launch_new_instance()
 if choice == 3:   install_nginx()
 if choice == 4:   
     copy_webserver_script()
     make_executable()
 if choice == 5:   install_python() 
 if choice == 6:   run_webserver_script()
 if choice == 7:   stop_instance()
 if choice == 8:   terminate_instance()
 if choice > 8: 
     print('\n\nPlease choose a valid option\n\n')
     main_menu()

def options():
 print('1: launch new instance and execute all services')
 print('2: launch new instance only')
 print('3: Install Nginx')
 print('4: Copy Nginx webserver script using SCP')
 print('5: Install Python 3 on instance')
 print('6: Run script to check if Nginx is running and start if not')
 print('7: Stop Instance')
 print('8: Terminate Instance')

def main_menu():
 options()
 choice = input('which task to you want to perform? ')
 int_choice = int(choice)
 choose_task(int_choice)

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
     print('variable is %d' % (execute_all))
 if execute_all == 1:
     execute_all_services()
 else:  
     main_menu()
     
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
     if run_remote_command(remote_host, key, cmd) == bool(0):
         print('Failure installing nginx')
 else:
     print('\nYou need to launch an instance first! \n\n')
     main_menu()
 if execute_all == 0:
     main_menu()
     
def copy_webserver_script():
 if instance != None:
     cmd = "scp -i " + key + " start_webserver.py " + full_remote_host +":."  
     if run_remote_command(remote_host, key, cmd) == bool(0):
         print('Failure copying webserver script.... Exiting..')
         sys.exit(1)
 else:
     print('\nYou need to launch an instance first! \n\n')
     main_menu()
 if execute_all == 0:
     main_menu()

def make_executable():
 if instance != None:
     cmd = "ssh -t -i " + key + " " + full_remote_host +" 'chmod 700 start_webserver.py'"
     if run_remote_command(remote_host, key, cmd) == bool(0):
         print('Failure copying webserver script')
         sys.exit(1)
 else:
     print('\nYou need to launch an instance first! \n\n')  
     main_menu()
 if execute_all == 0:
     main_menu()

def install_python():
 if instance != None:
     cmd = "ssh -t -i " + key + " " + full_remote_host + " 'sudo yum install -y python34'"
     if run_remote_command(remote_host, key, cmd) == bool(0):
         print('Failure installing python')
 else:
     print('\nYou need to launch an instance first! \n\n')  
     main_menu()
 if execute_all == 0:
     main_menu()

def run_webserver_script():
 if instance != None:
     cmd = "ssh -t -i " + key + " " + full_remote_host +" python3 start_webserver.py"
     if run_remote_command(remote_host, key, cmd) == bool(0):
         print('Failure installing python')
 else:
     print('\n You need to launch an instance first! \n\n')  
     main_menu()
 if execute_all == 0:
     main_menu()

def get_instance_info():
 if instance != None:
     print('\nconnection to zone: ', conn)
     print('\nreservation id: ', reservation)
     print('\ninstance : %s' % instance.id,  ' state is: %s' % instance.state, ' ip address is: %s \n'% instance.ip_address)
 else:
     print('\nYou need to launch an instance first! \n\n')  
     main_menu()
 if execute_all == 0: 
     main_menu()

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
         main_menu()
 else:
     print('\nYou need to launch an instance first! \n\n')  
     main_menu()

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
         main_menu()
 else:
     print('\nYou need to launch an instance first! \n\n')  
     main_menu()


def main(): 
 logger_main()
 main_menu()

if __name__ == '__main__':
  main()

  #var/log/ngnix/access.log