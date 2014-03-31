#scans the file directory for the file INFO to get the the list of programs  to be installed.
#parameter : Filepath
#Note: the content of the file should be in JSON method.

#!/usr/bin/python

#include the import modules

import sys
import os
import json
from pprint import pprint
import getpass
from os.path import expanduser

#Root path where the programs are stored 
path= expanduser("~")
path=path+"/wsl_programs"
#path where the program list is saved
filepath=path+""



def Sqltuple():
#scan for all files
  print "Inside sqltuple"
  files=[]
  for dirname, dirnames, filenames in os.walk(path):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
    #    print os.path.join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
     files.append(os.path.abspath(os.path.join(dirname, filename)))

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
   #if '.git' in dirnames:
    # don't go into any .git directories.
    #   dirnames.remove('.git')

  #look for the file with name INFO each directory
  print "intermediate"
  programs=[]
  for f in files:
    if f.endswith("INFO"):
      #read a json structure and form the tuple 
      #print f
      # take the file dir and the JSON data as a tuple
      content=open(f)
      j=json.load(content) # dir(j) is a dict ?
      programs.append((j['program name'],j['version'],j['comment'],f[:-5]))
      content.close()
  
  
  return programs     

    
   
def main():
  print "current directory :"+os.getcwd()
  print "current user"+getpass.getuser()
  print "Search directory"+path
  print "scan_program started"
  Sqltuple()

if __name__ == '__main__':
    main()  
