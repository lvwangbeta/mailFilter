# -*- coding: utf-8 -*-
import socket
import sys

if __name__ == '__main__':
	host = 'localhost'
	port = 8888
	try:
		fi = str(sys.argv[1])
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		msg = open(fi).read()
		s.connect((host, port))
		s.sendall(msg)
		s.close()		
	except:
		print "error: Input the email location"

