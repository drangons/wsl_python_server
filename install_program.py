#!/usr/bin/python

# connect to the sqlite db

import sqlite3
import os
import subprocess
import sys
import time


def install_program(path):


  #Go to the directory
  os.chdir(path) # possible exception.
  # os.getcwd() # get current working directory

  f = open('compile.log', 'w')
  # reset the base station 
  result=subprocess.call('tos-deluge serial@/dev/ttyUSB1:57600 -b',shell=True)# send the ouput to file

  if result !=0:
    print "reset the base station?"
  #ping before you issue commands  
  #build the application
  result=subprocess.call('make iris',stdout=f, stderr=subprocess.STDOUT, shell=True)
  if result !=0:
    print "Error in building application"
    
  # install the program on base station volume
  result=subprocess.call('tos-deluge serial@/dev/ttyUSB1:57600 -i 2 build/iris/tos_image.xml',stdout=f,          stderr=subprocess.STDOUT,shell=True) #allout.txt 2>&1 # use the subprocess module here

  if result !=0:
    print "Error in installing the program to base station"
    #pass


  # dessimate the program in volume 2
  # should i have to put a wait afer this command or use the command after this directly ?
 # result=subprocess.call('tos-deluge serial@/dev/ttyUSB1:57600 -d 2 ',stdout=f, stderr=subprocess.STDOUT, shell=True)

  #update the json database here.
  
  if result !=0:
    print "Error in dessimating the program"
  print "sleep for 10 second"
  time.sleep(10)  
  #instruct the remote mote to install the program in volume 2
  result=subprocess.call('tos-deluge serial@/dev/ttyUSB1:57600 -dr 2 ', stdout=f, stderr=subprocess.STDOUT, shell=True) 
  
  # there got to be an delay here.

  if result !=0:
    print "Error in reprogramming"

  f.close()


def main():
  print "program_start"
  print sys.argv[1]
  install_program(sys.argv[1])
  
  
if __name__ == '__main__':
    main()  


