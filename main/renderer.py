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

                    response = Stream(resourceName)

                    # Render the response

                    # If resource found send 200 SUCCESS response to controller

                    response = json.dumps({"MessageType": MessageType.RESPONSE, "ServerIP": str(NodeAddresses.serverIP), "RCSTVersion": "1.0", "status": "200 SUCCESS",
                                           "payload": resourceName + " has been rendered"})
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

            elif messageType == MessageType.RESPONSE:

                print("This is the response of an RCST request message")

            elif messageType == MessageType.CLOSE:

                print("Renderer is shutting down")
                serverIsOn = False

        except IOError as err:

            # If an error is present send the message to the controller and close the socket

            print("IOError: " + str(err))

        # Close connection socket after handling message
        conn.close()

    # close server socket

    rendererSocket.close()


def Stream(resource):
    print("Streaming " + resource)

    return True


startListening()
