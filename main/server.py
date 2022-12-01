'''
This is the server class, it listens for requests
from the controller and receiver

For the controller, it returns a list of files
For the renderer it streams the files to it

'''
# import dependencies

import socket
import json
import os
from os import listdir
from os.path import isfile, join
import sys
import rcst_protocol_util
from rcst_protocol_util import *

# get the path of the folder holding the media files

mediaFolder = os.path.normpath("files")
server_host = '127.0.0.1'
server_port = 5000
# server functions

# this function starts the server and listens for requests


def startListening():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket initialized")

    # listen to two hosts at a time, renderer and controller

    # Try to bind

    try:
        serverSocket.bind(
            (NodeAddresses.serverIP, NodePorts.serverPort))
        print("Socket bind is successful..")
    except socket.error as msg:

        print("Bind was uncessful. Error: " + str(msg))
        sys.exit()

    # After the bind is sucessful, start listening

    serverSocket.listen(2)

    print("Server listening on port " + str(NodePorts.controllerPort))

    # Turn the server on

    serverIsOn = True

    while serverIsOn:

        # Establish a connection

        conn, addr = serverSocket.accept()

        print("Connected to {0} \nListening on port {1}".format(
            str(addr), str(NodePorts.serverPort)))

        try:

            # receive message from the socket

            message = conn.recv(1024)

            # There are three types of requests, RETRIEVE, RENDER AND STREAM
            # For request messages
            # Get the RCST request type, get the fileName and all useful information from request line
            # { "MessageType": < val >, "ResourceName": < val >, "ServerIp" : <val>, "RCSTVersion": <val> }
            # For each request there is a corresponding response
            # For controller to server when initiating RETRIEVE, the response from the server is a response line and a payload
            # decode the message

            message = message.decode('utf-8')

            message = json.loads(message)

            print(message)

            # capture request type

            messageType = message['MessageType']

            print(messageType)

            # capture the fileName

            resourceName = message['ResourceName']

            print(resourceName)

            if messageType == MessageType.RETRIEVE:

                print("Retrieve a list")

            elif messageType == MessageType.RENDER:

                print("Render a media file")

            elif messageType == MessageType.STREAM:

                print("Stream a media file")

            elif messageType == MessageType.RESPONSE:

                print("This is the response of an RCST request message")

            elif messageType == MessageType.CLOSE:

                print("Server is shutting down")
                serverIsOn = False

        except IOError as err:

            # If an error is present send the message to the controller and close the socket

            print("IOError: " + str(err))

        # Close connection socket after handling message
        conn.close()

    # close server socket

    serverSocket.close()


startListening()
