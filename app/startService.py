from typing import Union
from fastapi import FastAPI
import socketio
from time import sleep
import hashlib
from pydantic import BaseModel

TemiWebSocket = FastAPI()

sio = socketio.Client()

class EmitData(BaseModel):
    serialNo: str
    password: str

@sio.event
def connect():
    return ("I'm connected!")

@sio.event
def disconnect():
    return ("I'm disconnected!")

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
    print(data)
    return (data)

@TemiWebSocket.post('/temi/emit')
async def reply_hello_world(EmitData: EmitData):
    sio.connect('https://api.robocore.ai', socketio_path='/remote')
    sleep(2)
    print('TESTING')
    #response = emitPairTemi("00119452331", "robocore")
    response = emitPairTemi(EmitData.serialNo, EmitData.password)
    sleep(2)
    sio.disconnect()
    return {"message": response}