import socket
import sys
import json
import rcst_protocol_util
# import protocol methods
from rcst_protocol_util import *


request = {'messageType': 'RETRIEVE'}


toBytes = convertToBytes(request)

print(convertToBytes)
