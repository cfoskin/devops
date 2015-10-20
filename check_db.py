#!/usr/bin/python3
import subprocess

def check_db():
 cmd = 'ps -A | grep mysql'
 run_mysql = 'sudo service mysqld start'
 (status,output) = subprocess.getstatusoutput(cmd)
 if status:
     reply = input('NOT RUNNING, would you like to start mysql - y/n?')
     if reply == 'y':
         (mysql_status, mysql_output) = subprocess.getstatusoutput(run_mysql)
         print('mysql started, now : RUNNING')
 else:
     print('RUNNING')


def main():
    check_db()

if __name__ == '__main__':
  main()

