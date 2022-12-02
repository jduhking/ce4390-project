# This file holds all the necessary functions needed to carry out our protocol

import json


class NodeAddresses:
    controllerIP = "10.0.0.1"
    serverIP = "10.0.0.2"
    rendererIP = "10.0.0.3"


class NodePorts:
    serverPort = 5000
    rendererPort = 3000
    controllerPort = 2000


class MessageType:

    RETRIEVE = 0
    RENDER = 1
    STREAM = 2
    CLOSE = 3
    RESPONSE = 4
