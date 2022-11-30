import socket
import sys
import json
import rcst_protocol_util
# import protocol methods
from rcst_protocol_util import *


request = {'messageType': 'RETRIEVE'}

request = json.dumps(request)

stringJSON = json.dumps(request)

print(json_loads_bytes(stringJSON))
