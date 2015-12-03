#colum foskin 
#!/usr/bin/python3
#a python program to create a file to log errors to.

import logging
import time

#log the error message to file. used in ssh helper.py.
def log_to_file(output, status):
 current_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
 logging.info('Date and Time: '+ current_time + " Output: " + output + "\nStatus Code: %d" % status + '\n')

#create the error log file. this is only run once in main of the main program - run_web_server.py.
def create_log_file(): 
 logging.basicConfig(filename='ec2_errors.log',level=logging.INFO)
