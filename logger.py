#colum foskin 20062042
#!/usr/bin/python3
#a python program to create a file to log errors to.

import logging
import time

def log_to_file(output, status):
 current_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
 logging.info('Date and Time: '+ current_time + " Output: " + output + "\nStatus Code: %d" % status + '\n')

def create_log_file(): 
 logging.basicConfig(filename='ec2_errors.log',level=logging.INFO)
