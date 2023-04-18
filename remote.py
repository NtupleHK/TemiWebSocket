import hashlib
from time import sleep
import socketio

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def connect_error(data):
    print("The connection failed!")
    print(data)

@sio.event
def message(data):
    print('I received a message!')

@sio.on("temiLocations")
def onTemiLocationsReceived(data) :
    print("[onTemiLocationsReceived]")
    print(data)

def emitPairTemi(serialNo: str, password: str):
    hashedPass = hashlib.sha256("robocore".encode("utf-8")).hexdigest()
    data = "{serialNo}:{hashedPass}".format(serialNo=serialNo, hashedPass=hashedPass)
    sio.emit("pairTemi", data)

sio.connect('https://api.robocore.ai', socketio_path='/remote')
sleep(5)
emitPairTemi("00119452331", "robocore")
sleep(5)
sio.disconnect()