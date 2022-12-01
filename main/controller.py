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

# controller functions


def getInput():  # get user input and send a request based on that input

    menuOptions = ("Welcome to the controller interface: Select an option\n"
                   "1) Get list of media files from the server"
                   "2) Open the file. \n"
                   "3) Close. \n")

    while True:  # block until user has entered a value
        try:  # enter the value
            userInput = int(
                input(menuOptions + "\n" + "Please select an option: "))
        except ValueError:
            print("Wrong Input, try again")
            continue  # continually prompt for input until correct value is entered
    # Make sure if the input is within the range

        if userInput < 1 or userInput > 3:
            print("Invalid option, try again")
        else:  # Once the correct input is selected, then break out of validation loop
            break
    return userInput

# Send a request to the server to retreive a list of media files located on the server


def RetrieveFiles(folderName):
    # Create RCST request message for getting the list of files

    request = json.dumps({"MessageType": MessageType.RETRIEVE,
                         "ResourceName": str(folderName), "ServerIP": "127.0.0.1", "RCSTVersion": "1.0"})
    request = request.encode('utf-8')
    # Create socket

    controllerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server socket

    controllerSocket.connect((NodeAddresses.serverIP, NodePorts.serverPort))

    # send request to server

    controllerSocket.sendall(request)

    # await the response and store it

    response = controllerSocket.recv(1024)

    # close the socket

    controllerSocket.close()

    # Run the controller functions

    # get the input and then perform a function depending on the value

    # Get the data, convert back into python dictionary

    response = response.decode('utf-8')
    response = json.loads(response)

    if response["status"] == "404 CANT FIND":

        # check if the response is an error response, if so output the status of the response and the error msg

        print(response["status"])
        print(response["payload"])

    else:
        # if not Display the list of files and the status

        print(response["status"])

        outputtedList = response["payload"]

        for file in outputtedList:
            print(file)

# send a request to the server and renderer to shut down, shut down only after BOTH server and renderer have shut down


def Shutdown():

    print("HELLO world")

    var = True

    return var


controllerInput = int

while controllerInput != 3:
    controllerInput = getInput()

    if controllerInput == 1:  # Get the list of media files
        # prompt the user to enter directory name
        folderName = input("Enter in the name of the folder: ")
        RetrieveFiles(folderName)

    elif controllerInput == 3:

        shutdown = Shutdown()

        if shutdown is True:
            sys.exit()
        else:
            print("Oops! An error occured in the process of shutting down \n")
