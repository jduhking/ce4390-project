# ce4390-project
## RCST Protocol - (Receiver Controller Server Transmission Protocol)

Application Protocol for transmitting data over virtual network between a controller, renderer and server.

The purpose of this protocol is to allow a controller (C) to request (RETRIEVE) a list of media files from a server (S) and can request R to render the chosen file (RENDER). The receiver (R), upon receiving a request from the controller (C), sends a request to the server (S) who then streams (STREAM) the chosen media file to R for rendering. 

LIMITATIONS:

- R CANNOT BUFFER, Renders what it receives from S.
- During streaming session, C can request R to pause/resume/start-from-the-beginning of the streaming

RCST Protocol Requests

'RETRIEVE' -> Get a list of media files from a server


'RENDER' -> Send a render request of a specific media file on a host


'STREAM' -> Render a specific media file from a server

# RCST Protocol Diagram

![alt text](https://github.com/jduhking/ce4390-project/blob/main/RCST%20protocol%20prototype.png?raw=true)
