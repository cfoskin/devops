#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2

def run_remote_command(remote_host,full_key_name, cmd):
 print('this is in other  class')
 (status,output) = subprocess.getstatusoutput(cmd)
 if not status:
     print("status:", status)
     print("Successful")
 else:
     print('status: ',status)
     print ("Error")
