#colum foskin 20062042
#!/usr/bin/python3
import logging
import time

def log_to_file(string):
 current_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
 logging.info('Date and Time: '+ current_time + " " + string +'\n')

def print_to_console(String):
 print(string)

def logger_main(): 
 logging.basicConfig(filename='ec2.log',level=logging.INFO)

#main_menu()

if __name__ == '__main__':
  logger_main()