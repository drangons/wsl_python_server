#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import subprocess 
from os import curdir, sep , path
from scan_programs import Sqltuple
import cgi
from install_program import install_program
import Queue
import threading
import shutil

PORT_NUMBER = 38080
SERVER_NAME=''
base_station="/home/android/wsl_programs/DelugeBasestation"
copmpile_log=''
program_path=""

class ThreadClass(threading.Thread):
  def run(self):
    install_program(program_path)
    print "Finished executing program %s on thread %s"%(program_path,self.getName())  

programs=[]
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
  
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/plain")
    s.end_headers()
  def do_GET(self):
    #send the json file
    print 'path ' + self.path
    mimetype='text/plain'
    #self.send_header('Content-type',mimetype)
    try:
      if self.path =='/':
	self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
	for program in programs:
	  self.wfile.write(program[0]+"\n")
        

      elif self.path == '/compile':
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
	print compile_log
	if path.isfile(compile_log):
  	  f=open(compile_log,"r")
          self.wfile.write(f.read())
          self.wfile.write("\n")
	  f.close()
	else:
          self.wfile.write("compile log not found in prgram directory\n")
	

      elif "program" in self.path :
	url=self.path
        idx=url.split("=")
	program_index=int(idx[-1])
        program=programs[program_index]
	global program_path
	program_path=program[-1]
	t=ThreadClass()
	t.start()
	src=program_path+"/compile.log"
	print src
	global compile_log
	compile_log=src	
	self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        

      elif self.path == '/result':
	print base_station
	result_path=base_station+"result.txt"
	if path.isfile(result_path):
	  f=open(result_path,"r")
          self.wfile.write(f.read())
	  self.wfile.write("\n")
	  f.close()
	else:
	  self.wfile.write("result file not found in Basestation directory\n")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
	
      else:
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(" No service implemented at :"+self.path)
        self.wfile.write("\n")
    except IOError:
      self.send_error(404, 'file not found')
    
    self.send_header('Content-Type',mimetype)
    #self.end_headers()
    self.send_response(200)
    return
  
    
try:
	#Create a web server and define the handler to manage the
	#incoming request
	programs=Sqltuple()
	server = HTTPServer((SERVER_NAME, PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
