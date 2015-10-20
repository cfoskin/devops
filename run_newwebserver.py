#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import boto.manage.cmdshell
import time
import socket
from logger import * 

def choose_task(choice):
 if choice == 1:   launch_new_instance()

def main_menu():
 print('1: launch new instance')
 choice = input('which task to you want to perform? ')
 int_choice = int(choice)
 choose_task(int_choice)

def launch_new_instance():
 key = 'cfoskin_key'
 conn = boto.ec2.connect_to_region("eu-west-1")
 reservation = conn.run_instances('ami-69b9941e', key_name = key, instance_type = 't2.micro', security_groups = ['witsshrdp'])
 instance = reservation.instances[0]
 instance.add_tag('Name','GA_ColumFoskin')
 print('launching new instance, This may take a few minutes....')
 while instance.state != 'running':
     time.sleep(10)
     log_to_file(instance.update())
 else:
     get_instance_info(instance,conn,reservation)

 reply = input('Do you want to shut down and terminate the instance y/n? ')
 if reply == 'y':
     log_to_file('stopping instance now...')
     instance.terminate()
     while instance.state != 'terminated':
         time.sleep(10)
         print(instance.update())
     else:
         print('instance is stopped and terminated')
 else: 
     print('Proceedng with installation of nginx...')
     print('attempting to connect to instance using ssh...')
     public_ip = instance.ip_address
     remote_host = "ec2-user@" + public_ip  
     full_key_name = key + '.pem'  
     install_nginx(remote_host, full_key_name)


def get_instance_info(instance, conn, reservation):
 print('connection to zone: ', conn)
 print('reservation id: ', reservation)
 print('instance : %s' % instance.id,  ' state is: %s' % instance.state, ' ip address is: %s'% instance.ip_address)

def install_nginx(remote_host, full_key_name):
 time.sleep(20)
 cmd = " ssh -t -o StrictHostKeyChecking=no -i " + full_key_name + " " + remote_host + " 'sudo yum install -y nginx' "
 success = bool(0)
 while not success:#keep trying until successful as it was only connecting sometimes.
     (status,output) = subprocess.getstatusoutput(cmd)
     if not status:
         print('Output nginx: ', output)
         success = bool(1)
         copy_webserver_script(remote_host, full_key_name)
     else: print(output, 'Error installing nginx')#failing here a LOT before it is successful?
     
def copy_webserver_script(remote_host, full_key_name):
 cmd = "scp -o StrictHostKeyChecking=no -i " + full_key_name + " check_webserver.py " + remote_host + ":."  
 (status,output) = subprocess.getstatusoutput(cmd)
 if not status:
     print('scp was successful')
     manage_webserver_script(remote_host, full_key_name)
 else:
     print('output: ',output)
     print ("Error from scp")

def manage_webserver_script(remote_host,full_key_name):
 chmod_cmd = "ssh -t -o StrictHostKeyChecking=no -i " + full_key_name + " " + remote_host + " 'chmod 700 check_webserver.py'"
 (status,output) = subprocess.getstatusoutput(chmod_cmd)
 if not status:
     print("status:", status)
     print("permissions successfully changed on script")
     install_python(remote_host,full_key_name)
 else:
     print('status: ',status)
     print ("Error changing permissions")

def install_python(remote_host,full_key_name):
 install_python_cmd = "ssh -t -o StrictHostKeyChecking=no -i " + full_key_name + " " + remote_host + " 'sudo yum install -y python34'"
 (status,output) = subprocess.getstatusoutput(install_python_cmd)
 if not status:
     print('install python status: ',status)
     print(output + " Python 3 successfully installed...")
     run_webserver_script(remote_host,full_key_name)
 else:
     print('status: ',status)
     print ("Error installing python")

def run_webserver_script(remote_host,full_key_name):
 run_script_cmd = "ssh -i " + full_key_name + " " + remote_host + " 'python3 check_webserver.py'"
 print(run_script_cmd)
 (status,output) = subprocess.getstatusoutput(run_script_cmd)
 if not status:
     print('run script status: ',status)
     print(output)
 else:
     print('status: ',status)
     print ("Error running script")

def main(): 
 logger_main()
 launch_new_instance()

#main_menu()

if __name__ == '__main__':
  main()