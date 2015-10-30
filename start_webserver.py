#!/usr/bin/python3
#A tiny Python program to check that nginx is running and start it if not, this program was given
#to us and not written by me.
import sys
import subprocess

#check if nginx is running and start if it is not. 
def startnginx():
    cmd = 'ps -A | grep nginx' 

    (status, output) = subprocess.getstatusoutput(cmd)

    if status == 0:  
        print ("Nginx server is already running")
        sys.exit(1)
    else:
        sys.stderr.write(output)
        print ("Nginx Server not running, so let's try to start it now...")
        cmd = 'sudo service nginx start'
        (status, output) = subprocess.getstatusoutput(cmd)
        if status:
            print ("--- Error starting nginx! ---")
            sys.exit(2)
        print ("Nginx started successfully")
        sys.exit(0)

# Define a main() function.
def main():
    startnginx()
      
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

