#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import boto
import boto.ec2

def run_remote_command(remote_host, key, cmd):
 (status,output) = subprocess.getstatusoutput(cmd)
 if status >0:
     print("status:", status)
     return bool(0)
 else:
     print("status:", status)
     print(output)
     return bool(1)