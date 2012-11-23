# -*- coding: utf-8 -*-
import socket

if __name__ == '__main__':
    host = 'localhost'
    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = open(r"./email.txt").read()
    s.connect((host, port))
    s.sendall(msg)
    s.close()
