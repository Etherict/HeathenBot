import socket
import logging
import sys
import time
import random
import re
import operator
import csv
import datetime

logging.basicConfig(filename='log' + str(datetime.datetime.now().date()) + '.log',level=logging.INFO)

def logMsg(msg):
    logging.info(str(datetime.datetime.now()) + ": " + str(msg))

#respond to server pings
def ping(pingData, ircs):
    pong = "PONG :" + pingData
    logMsg(pong)
    pong = pong + '\r\n'
    ircs.send(pong.encode('utf-8'))

#send private message
def sendChanMsg(chan, msg, ircs):
    logMsg("Sending message: " + msg)
    ircs.send(("PRIVMSG " + chan + " :" + msg + "\r\n").encode('utf-8'))

#join a channel
def joinChan(chan, ircs):
    ircs.send(("JOIN " + chan + "\r\n").encode('utf-8'))
    
def mute(periodToMute):
    time.sleep(periodToMute)
