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
        print("Socket bind was successful..")
    except socket.error as msg:

        print("Bind was uncessful. Error: " + str(msg))
        sys.exit()

    # After the bind is sucessful, start listening

    serverSocket.listen(2)

    print("Server listening on port " + str(NodePorts.serverPort))

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

            # capture request type

            messageType = message['MessageType']

            # capture the fileName

            resourceName = message['ResourceName']

            if messageType == MessageType.RETRIEVE:

                # retrieve the list of files
                try:

                    fileList = retrieveList(resourceName)

                    # Generate the response message which takes the form of

                    # { "MessageType" : "RESPONSE", "ServerIP" : < val >, "RCSTVersion" : "1.0", "payload" : <any>  }
                    # And comes attached with a payload

                    response = json.dumps({"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "200 SUCCESS",
                                           "payload": fileList})
                    response = response.encode('utf-8')

                    print(response)

                    conn.sendall(response)

                except OSError as osErr:  # If file not found send an error response

                    errorResponse = json.dumps(
                        {"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "404 CANT FIND",
                         "payload": str(osErr)}
                    )

                    print(errorResponse)

                    errorResponse = errorResponse.encode(
                        'utf-8')  # encode into bytes

                    conn.sendall(errorResponse)

            elif messageType == MessageType.RENDER:

                print("Render a media file")

            elif messageType == MessageType.STREAM:

                print("STREAMING START")
                print(resourceName)
                # stream request gets passed a resource object containing the path and the name of the resource under the resourceName section

                resourcePath = resourceName['resourcePath']
                resource = resourceName['resource']

                print("Attempting to retrieve " +
                      str(resource) + " at " + str(resourcePath))

                try:

                    payload = streamResource(resourcePath, resource)

                    response = json.dumps(
                        {"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "200 SUCCESS",
                         "payload": payload})

                    response = response.encode('utf-8')

                    conn.sendall(response)

                except OSError as e:

                    errorResponse = json.dumps(
                        {"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "404 CANT FIND",
                         "payload": "File / Directory could not be found"})

                    errorResponse = errorResponse.encode('utf-8')

                    conn.sendall(errorResponse)

            elif messageType == MessageType.RESPONSE:

                print("This is the response of an RCST request message")

            elif messageType == MessageType.CLOSE:

                print("Server is shutting down")
                # send success message back to controller

                response = json.dumps(
                    {"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "200 SUCCESS",
                     "payload": "The server is shutting down..."}
                )

                response = response.encode('utf-8')

                print(response)

                conn.sendall(response)

                serverIsOn = False

        except IOError as err:

            # If an error is present send the message to the controller and close the socket

            print("IOError: " + str(err))

        # Close connection socket after handling message
        conn.close()

    # close server socket

    serverSocket.close()

# this function retrieves a list of media files in a given directory


def retrieveList(folderName):

    # get the path of the folder holding the media files

    path = os.path.normpath(folderName)

    # get the list of files in a folder

    fileList = [f for f in listdir(
        path) if isfile(join(path, f))]

    # sort the files in ascending order

    fileList.sort()

    return fileList


def streamResource(resourceDirectory, resourceName):

    # Get the path of the resource

    path = os.path.normpath(resourceDirectory)

    # Open file in read-binary
    file = open(join(path, resourceName), "rb")

    payload = file.read()
    print(payload)
    payload = payload.decode('utf-8')
    return payload


startListening()
