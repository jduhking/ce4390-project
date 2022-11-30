# This file holds all the necessary functions needed to carry out our protocol

import json


class messageTypes:

    RETRIEVE = 0
    RENDER = 1
    STREAM = 2
    CLOSE = 3
    RESPONSE = 4


# function to convert the data into bytes


def convertToBytes(payload, ignoreDictionary=False):

    # This function converts our data into bytes to sent over network

    if isinstance(payload, str):  # return a single bytified value
        return payload.encode('utf-8')

    if isinstance(payload, list):  # if it is a list of values return a list of bytified value
        return [convertToBytes(data, ignoreDictionary=True) for data in payload]
    # if the data is a dictionary return a dictionary of bytified key and value pairs

    if isinstance(payload, dict) and not ignoreDictionary:

        return {

            convertToBytes(key, ignoreDictionary=True): convertToBytes(value, ignoreDictionary)
            for key, value in payload.items()
        }

    # spit the unchanged data back if it is not applicable

    return payload
