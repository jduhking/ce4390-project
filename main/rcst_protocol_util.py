# This file holds all the necessary functions needed to carry out our protocol

import json


class NodeAddresses:
    controllerIP = "127.0.0.1"
    serverIP = "127.0.0.1"
    rendererIP = "127.0.0.1"


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

# function to convert json data into dictionary


def json_load_bytes(fileName):

    return convertToBytes(

        json.load(fileName, object_hook=convertToBytes),
        ignoreDictionary=True
    )

# if the data is in the form of a JSON string the convert it to a dictionary


def json_loads_bytes(json_text):

    return convertToBytes(
        json.loads(json_text, object_hook=convertToBytes),
        ignoreDictionary=True
    )

# function to convert the data into bytes


def convertToBytes(message, ignoreDictionary=False):

    # This function converts our data into bytes to sent over network

    if isinstance(message, str):  # return a single bytified value

        return message.encode('utf-8')

    if isinstance(message, list):  # if it is a list of values return a list of bytified value

        return [convertToBytes(data, ignoreDictionary=True) for data in message]
    # if the data is a dictionary return a dictionary of bytified key and value pairs

    if isinstance(message, dict) and not ignoreDictionary:

        return {
            convertToBytes(key, ignoreDictionary=True): convertToBytes(value, ignoreDictionary=True)
            for key, value in message.items()
        }

    # spit the unchanged data back if it is not applicable

    return message
