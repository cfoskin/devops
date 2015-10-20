#colum foskin 20062042
#!/usr/bin/python3
import subprocess
import os

def count_processes():
 cmd_count_processes = 'ps -AL --no-headers | wc -l'
 (status,output) = subprocess.getstatusoutput(cmd_count_processes)
 if not status :
     return int(output)

def display_vm_stats():
 cmd_vmstat = 'vmstat'
 (status,output) = subprocess.getstatusoutput(cmd_vmstat)
 if not status:
     return output

def netstat():
 cmd_netstat = 'netstat -an | more'
 (status,output) = subprocess.getstatusoutput(cmd_netstat)
 if not status:
     return output

def check_performance():
 cmd_top = 'top'
 # the subprocesses wouldnt work here for me for some reason so i used os.system 
 # (status,output) = subprocess.getstatusoutput(cmd_top)
 # if status:
 #     return output
 os.system(cmd_top)

def options():
 print('1: count processes')
 print('2: check performance')
 print('3: check virtual memory stats')
 print('4: check network statistics')

def choose_task(choice):
 if choice == 1:   print('no of processes running is: ', count_processes())
 elif choice == 2: check_performance()
 elif choice == 3: print(display_vm_stats())
 elif choice == 4: print(netstat())

def main():
    options()
    choice = input('which task to you want to perform? ')
    int_choice = int(choice)
    choose_task(int_choice)
if __name__ == '__main__':
  main()