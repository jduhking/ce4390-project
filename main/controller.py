import socket
import sys
import json
import rcst_protocol_util
# import protocol methods
from rcst_protocol_util import *

'''

 This controller displays a menu of options for the user 
 Can request a list of files located on a server
 Can send a render request for a renderer to stream a file located 
 on a server

 Protocol used is the RCST protocol

'''

# important variables

server_host = '127.0.0.1'  # IP of the server
server_port = 5000  # server port

# controller functions


def getInput():  # get user input and send a request based on that input

    menuOptions = ("Welcome to the controller interface: Select an option\n"
                   "1) Get list of media files from the server"
                   "2) Open the file. \n"
                   "3) Close. \n")
    '''
        while True:  # block until user has entered a value
    try:  # enter the value
        userInput = int()
    '''


# wait for user input and send requests based on that
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_host, server_port))
    s.sendall(b'Hello!, world')
    data = s.recv(256)

print('Received', repr(data))
