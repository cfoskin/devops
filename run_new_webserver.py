#colum foskin 20062042
#!/usr/bin/python3
#this python program allows a user to interact with aws using boto. It allows them to remotely launch 
#an ec2 instance and then installs nginx and uses scp to copy a script using ssh remote. This can be done 
#automatically by choosing one option or on a step by step basis if the user chooses to do so.

import subprocess
import boto
import boto.ec2
import time
import sys
import os
from ssh_helper import run_remote_command 
from logger import create_log_file
from termcolor import colored
instance = None
instance_ip = ''
instance_dns =''
key = 'cfoskin_key.pem'
remote_host = "ec2-user@"
full_remote_host = ''
conn = ''
reservation=''
execute_all = 1

#opens the connection to the region specified and sets up the reservation
def connect():
    print('Opening connection - Please Wait......')
    global conn
    conn = boto.ec2.connect_to_region("eu-west-1")
    if conn:
        print('Connection Made \n')
    else:
        print('Error: failed to connect to EC2 region')

#Launches an instance and updates the user of its status until runnning, then break out if the user is 
#manually using the services provided otherwise execute all other services.
#The current set up only allows one instance per session so I have a small check here to 
#prevent going through the process of getting and tagging the same instance if the user 
#chooses launch instance moe than once. 
def launch_new_instance():
 global instance
 if instance != None:
     print('\n\n Instance Already Launched - Please Choose another option or restart program to launch a new instance')
 else:
     global reservation
     reservation = conn.run_instances('ami-69b9941e', key_name = 'cfoskin_key', instance_type = 't2.micro', security_groups = ['witsshrdp'])
     instance = reservation.instances[0]
     instance.add_tag('Name','GA_ColumFoskin')
     print('Instance Launching - Please wait for initialization... ')
     while instance.state != 'running':
         time.sleep(10)
         print(instance.update())
     else:
         print('Instance Launch Complete - Instance is Running \n')
         wait_for_ssh_service()
         get_instance_info()
         global instance_ip
         instance_ip = instance.ip_address
         global instance_dns 
         instance_dns = instance.public_dns_name
         global full_remote_host
         full_remote_host = remote_host + instance_ip
         if execute_all == 1:
             execute_all_services()

#execute all the services if the user has chosen that option
def execute_all_services():
 install_nginx()
 copy_webserver_script()
 make_executable()
 install_python() 
 run_webserver_script()

#sleep for 90 seconds to allow ssh to start.
def wait_for_ssh_service():
 print('Time sleep started while waiting for ssh and other services to start\n')
 time.sleep(100)#chose 100 to avoid breaking at demo as it was still hit and miss with 80/90.
 print('Time sleep finished......\n\n')


#install nginx using ssh remote cmd.
def install_nginx():
 print('\n Proceedng with installation of nginx now using ssh...\n')
 cmd = " ssh -t -o StrictHostKeyChecking=no -i " + key + " " + full_remote_host + " 'sudo yum install -y nginx' "
 while run_remote_command(instance, cmd) == bool(0): #ssh remote function from ssh helper class
     run_remote_command(instance, cmd)
 
#copy up the start webserver script using SCP which checks if nginx is running and starts if not.
def copy_webserver_script():
 cmd = "scp -i " + key + " start_webserver.py " + full_remote_host +":."  
 run_remote_command(instance,cmd)

#make the script executable.
def make_executable():
 cmd = "ssh -t -i " + key + " " + full_remote_host +" 'chmod 700 start_webserver.py'"
 run_remote_command(instance, cmd)

#install python 3.
def install_python():
 cmd = "ssh -t -i " + key + " " + full_remote_host + " 'sudo yum install -y python34'"
 run_remote_command(instance, cmd)

#run the script. 
def run_webserver_script():
 cmd = "ssh -t -i " + key + " " + full_remote_host +" python3 start_webserver.py"
 run_remote_command(instance, cmd)
 
#get the instance info for the user after a succesfull launch
def get_instance_info():
 if instance != None:
     print('\nconnection to zone: ', conn)
     print('\nreservation id: ', reservation)
     print('\ninstance : %s' % instance.id,  ' state is: %s' % instance.state, ' ip address is: %s \n'% instance.ip_address)
 else:
     print('\nYou need to launch an instance first! \n\n')  

#test the nginx page is there correctly by using lynx - i used os.system here 
#as for some reason the subprocesses way would not work with the same command.
def test():
 cmd = " lynx " + instance_dns
 os.system(cmd)

#view the nginx acces or error log files
def nginx_log():
 chown_cmd = "ssh -t -i " + key + " " + full_remote_host +" sudo chown ec2-user /var/log/nginx/"
 access_log_cmd = "ssh -t -i " + key + " " + full_remote_host +" cat /var/log/nginx/access.log"
 run_remote_command(instance, chown_cmd)
 run_remote_command(instance, access_log_cmd)

#view local ec2 error log file
def view_error_log():
 cmd = " cat ec2_errors.log "
 os.system(cmd)

#stop the instance
def stop_instance():
 if instance != None:
     if instance.state == 'running':
         instance.stop()
         while instance.state != 'stopped':
             time.sleep(5)
             print(instance.update())
         else:
             print('instance is stopped \n')
     else: 
         print('instance is not running! - cannot stop the instance \n')
 else:
     print('\nYou Have No Instances Running! \n\n')  

#terminate the instance
def terminate_instance():
 if instance != None:
     print('terminating instance now...')
     instance.terminate()
     while instance.state != 'terminated':
         time.sleep(5)
         print(instance.update())
     else:
         print('instance is stopped and terminated - Exiting.... \n')
         sys.exit(0)
 else:
     print('\nYou Have No Instances Running! \n\n')  

# a menu for the user
def options():
 choice = None
 while choice != '0':
     print(colored("\n\n Please Note -- If You are Manually Running The Services Listed -- You Must Execute Sequentially From 2 ===>>> 7   ", 'red',attrs=['reverse', 'blink']))
     print('=============                 Main Menu              =============')
     print('==================================================================')
     print(colored('|  1: launch new instance and execute all services                |', 'green'))
     print('|  2: launch new instance only                                    |')
     print('|  3: Install Nginx                                               |')
     print('|  4: Copy Nginx webserver script using SCP                       |')
     print('|  5: Change webserver script permissions                         |')
     print('|  6: Install Python 3 on instance                                |')
     print('|  7: Run script to check if Nginx is running and start if not    |')
     print('|  8: Stop Instance                                               |')
     print('|  9: Terminate Instance                                          |')
     print(colored('|  t: Test nginx is running correctly using lynx                  |','green'))
     print(colored('|  l: View  Nginx acces log file                                  |','green'))
     print(colored('|  e: View local ec2 error log                                    |','green'))
     print(colored('|  0: EXIT                                                        |', 'red'))
     print('==================================================================')
     choice = input('which task do you want to perform? \n\n ')
     if choice == '1':launch_new_instance()
     if choice == '2':   
         global execute_all 
         execute_all = 0#setting this variable to 0 here so when launching instance is called - the other funnctions won't be executed.
         launch_new_instance()
     if choice == '3': install_nginx()
     if choice == '4': copy_webserver_script()
     if choice == '5': make_executable() 
     if choice == '6': install_python() 
     if choice == '7': run_webserver_script()
     if choice == '8': stop_instance()
     if choice == '9': terminate_instance()
     if choice == 't': test()
     if choice == 'l': nginx_log()
     if choice == 'e': view_error_log()
     if choice == '0': sys.exit(0)    

def main():
 connect()
 create_log_file()#create the log file for error logging
 options()

if __name__ == '__main__':
  main()
