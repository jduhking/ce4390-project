'''
The renderer class sends streaming request to the server 
to display the file requested to render by the controller

'''
# Import dependencies

import base64
import json
import os
import socket
import sys
import rcst_protocol_util
from rcst_protocol_util import *

# Import functions


def startListening():

    rendererSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    rendererSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket initialized")

    try:

        rendererSocket.bind(
            (NodeAddresses.rendererIP, NodePorts.rendererPort))

        print("Socket bind was successful")
    except socket.error as errMsg:
        print("Bind was unsuccessful. Error: " + str(errMsg))
        sys.exit()

    # After the bind is sucessful, start listening

    rendererSocket.listen(2)

    print("Renderer listening on port " + str(NodePorts.rendererPort))

    rendererIsOn = True

    while rendererIsOn:

        # Establish a connection

        conn, addr = rendererSocket.accept()

        print("Connected to {0} \nListening on port {1}".format(
            str(addr), str(NodePorts.rendererPort)))

        try:

            # receive message from the socket

            message = conn.recv(1024)

            # Expecting RENDER requests or Stream Responses from the controller and server respectively
            # Get the RCST request type, get the fileName and all useful information from request line
            # { "MessageType": < val >, "ResourceName": < val >, "ServerIp" : <val>, "RCSTVersion": <val> }

            message = message.decode('utf-8')

            message = json.loads(message)

            # capture request type

            messageType = message['MessageType']

            # capture the fileName

            resourceName = message['ResourceName']

            if messageType == MessageType.RENDER:

                # If it is a render request, then initiate a stream request to the server
                try:

                    Stream(resourceName)

                    # If resource found send 200 SUCCESS response to controller

                    response = json.dumps({"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "200 SUCCESS",
                                           "payload": "The resource " + str(resourceName['resource']) + " has been rendered"})
                    response = response.encode('utf-8')

                    print(response)

                    conn.sendall(response)

                except Exception as err:  # If file not found send an error response

                    errorResponse = json.dumps(
                        {"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "500 CANNOT RENDER",
                         "payload": "The resource could not be rendered: " + str(err)}
                    )

                    print(errorResponse)

                    errorResponse = errorResponse.encode(
                        'utf-8')  # encode into bytes

                    # Send error response to controller
                    conn.sendall(errorResponse)

            elif messageType == MessageType.RESPONSE:

                print("This is the response of an RCST request message")

            elif messageType == MessageType.CLOSE:

                print("Renderer is shutting down")

                # Send a response to the controller notifying that the renderer shut down

                response = json.dumps(
                    {"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "200 SUCCESS",
                     "payload": "The renderer is shutting down..."}
                )
                response = response.encode('utf-8')
                # Create socket

                controllerSocket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

                try:
                    # Connect to server socket

                    controllerSocket.connect(
                        (NodeAddresses.controllerIP, NodePorts.controllerPort))

                    # send request to server

                    controllerSocket.sendall(response)
                except Exception as e:

                    print("Couldn't reach the controller")

                serverIsOn = False

        except IOError as err:

            # If an error is present send the message to the controller and close the socket

            print("IOError: " + str(err))

        # Close connection socket after handling message
        conn.close()

    # close server socket

    rendererSocket.close()


def Stream(resource):

    # Send request method to the server for streaming

    request = json.dumps({"MessageType": MessageType.STREAM,
                         "ResourceName": resource, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0"})

    print(str(request))
    request = request.encode('utf-8')
    print(str(request))
    # Create socket

    try:

        rendererSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Establishing connection with server....\n")
        # Connect to server socket

        rendererSocket.connect(
            (NodeAddresses.serverIP, NodePorts.serverPort))

        print("Connected to server \n")
        # send request to server

        rendererSocket.sendall(request)

        print("Sending stream request to server.... \n")

        # The renderer has no buffer, so it just renders all that it receives

        response = rendererSocket.recv(2048)

        # Render the data

        response = response.decode('utf-8')
        response = json.loads(response)

        if response["status"] == "200 SUCCESS":
            # Render the media file onto the screen

            print("Resource retrieved from the server....")
            data = response["payload"]

            print("Rendering the file... \n")
            print(resource)
            print("\n")
            print(data)
        else:

            # check if the response is an error response, if so output the status of the response and the error msg

            print(response["status"])
            print(response["payload"])

    except Exception as err:

        print("There was an error: " + str(err))


startListening()
