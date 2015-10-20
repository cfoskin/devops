#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2
import boto.manage.cmdshell
import time
from logger import * 
from ssh_helper import run_remote_command 
instance = None
instance_ip = ''
key = 'cfoskin_key.pem'
remote_host = "ec2-user@"

def choose_task(choice):
 if choice == 1:   launch_new_instance()

def main_menu():
 print('1: launch new instance')
 choice = input('which task to you want to perform? ')
 int_choice = int(choice)
 choose_task(int_choice)

def launch_new_instance():
 conn = boto.ec2.connect_to_region("eu-west-1")
 reservation = conn.run_instances('ami-69b9941e', key_name = 'cfoskin_key', instance_type = 't2.micro', security_groups = ['witsshrdp'])
 global instance
 instance = reservation.instances[0]
 instance.add_tag('Name','GA_ColumFoskin')
 while instance.state != 'running':
     time.sleep(10)
     print(instance.update())
     log_to_file(instance.update())
 else:
     #get_instance_info(conn,reservation)
     global instance_ip
     instance_ip = instance.ip_address
     install_nginx()


def get_instance_info(conn, reservation):
 print('connection to zone: ', conn)
 print('reservation id: ', reservation)
 print('instance : %s' % instance.id,  ' state is: %s' % instance.state, ' ip address is: %s'% instance.ip_address)


def shut_down_instance(instance):
 reply = input('Are you sure that you want to shut down and terminate the instance y/n? ')
 if reply == 'y':
     print('stopping instance now...')
     instance.terminate()
     while instance.state != 'terminated':
         time.sleep(10)
         print(instance.update())
     else:
         print('instance is stopped and terminated')
 else: 
 	 print('instance not shut down')


def install_nginx():
 print('Proceedng with installation of nginx...')
 print('attempting to connect to instance using ssh...')
 print('time sleep started while waiting for ssh to start')
 time.sleep(40)
 cmd = " ssh -t -o StrictHostKeyChecking=no -i " + key + " " + remote_host + instance_ip + " 'sudo yum install -y nginx' "
 success = bool(0)
 while not success:#keep trying until successful as it was only connecting sometimes.
     (status,output) = subprocess.getstatusoutput(cmd)
     if not status:
         print('Output nginx: ', output)
         success = bool(1)
         copy_webserver_script()
     else: print(output, 'Error installing nginx')#failing here a LOT before it is successful?


     
def copy_webserver_script():
 cmd = "scp -o StrictHostKeyChecking=no -i " + key + " check_webserver.py " + remote_host + instance_ip +":."  
 (status,output) = subprocess.getstatusoutput(cmd)
 if not status:
     print('scp was successful')
     manage_webserver_script()
 else:
     print('output: ',output)
     print ("Error from scp")

def manage_webserver_script():
 chmod_cmd = "ssh -t -o StrictHostKeyChecking=no -i " + key + " " + remote_host + instance_ip +" 'chmod 700 check_webserver.py'"
 (status,output) = subprocess.getstatusoutput(chmod_cmd)
 if not status:
     print("status:", status)
     print("permissions successfully changed on script")
     install_python()
 else:
     print('status: ',status)
     print ("Error changing permissions")

def install_python():
 install_python_cmd = "ssh -t -o StrictHostKeyChecking=no -i " + key + " " + remote_host + instance_ip + " 'sudo yum install -y python34'"
 (status,output) = subprocess.getstatusoutput(install_python_cmd)
 if not status:
     print('install python status: ',status)
     print(output + " Python 3 successfully installed...")
     run_webserver_script()
 else:
     print('status: ',status)
     print ("Error installing python")

def run_webserver_script():
 run_script_cmd = "ssh -i " + key + " " + remote_host + instance_ip +" 'python3 check_webserver.py'"
 start_nginx = "ssh -i " + key + " " + remote_host + instance_ip +" 'sudo service -y start nginx'"
 print(run_script_cmd)
 (status,output) = subprocess.getstatusoutput(run_script_cmd)
 if not status:
     print('run script status: ',status)
     print(output)
     if output == 'Nginx Server IS NOT running':
         (status2,output2) = subprocess.getstatusoutput(start_nginx)
         if not status2:
             print(output2)
         else: 
             print('Error starting nginx')
 else:
     print('status: ',status)
     print ("Error running script")

def main(): 
 logger_main()
 launch_new_instance()

#main_menu()

if __name__ == '__main__':
  main()

  #var/log/ngnix/access.log