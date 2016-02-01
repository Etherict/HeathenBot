import socket
import logging
import sys
import time
import random
import re
import operator
import datetime

from HeathenBotFunctions import *
from IRC_functions import *

server = "irc.esper.net"
channel = "#pagan"
botnick  = "HeathenBot"
modList = ['jimr1603','Etherict','hrafnblod','UsurpedLettuce','RyderHiME','HereticHierophant','manimatr0n','c_brighde','cmacis','MidDipper']

def decomposeMsg(ircData):
    logMsg("Full data is: " + ircData)
    chan = ircData.split(':')[1].split(' ')[2]
    logMsg("Channel is: " + chan)
    user = ircData.split(':')[1].split('!')[0]
    logMsg("User is: " + user)
    ircData = ircData.split(':')
    commands=ircData[2:]
    command=""
    for c in commands:
        command+=":"+c
    command=command[1:]
    #command = ",".join(ircData)
    logMsg("Command is: " + command)
    command = command.strip('.').strip()
    logMsg("Command received: " + command)
    logMsg('USER parsed as ' + user)
    return (user, chan, command)

def runCommand(user, chan, command, ircsock):
    if(command.lower()[0:len(botnick)]==botnick.lower()):
        command=command[len(botnick)+1:]
        while command[0]==" ":
            command=command[1:]
    try:
        commandTree(user, chan, command, ircsock)
    except SystemExit:
        close_database()
        logMsg(sys.exc_info())
        sys.exit()
    except:
        sendChanMsg(channel, "Good job, you broke me. Dumbass.", ircsock)
        logMsg(sys.exc_info())

def commandTree(user, chan, command, ircs):
    logMsg("CommandTree running: "+command)
    if chan == botnick:
        chan = user

    if user != botnick:
        if "convert" in command.lower():
            convertTemperatures(command, chan, ircs)
        elif "google" in command.lower():
            google(command, chan, user, ircs)
        elif "wiki" in command.lower():
            wiki(command, chan, user, ircs)
        elif "give me a hammer" in command.lower():
            giveHammer(chan, ircs)
        elif "cheers" in command.lower():
            raiseCheers(chan, ircs)
        elif "sing me a song" in command.lower():            
            singSong(chan, ircs)
        elif "be quiet" in command.lower() and user in modList:
            muteBot(command)
        elif "help" in command.lower():
            sendHelpToUser(user, chan, modList, ircs)
        elif "who's a mod" in command.lower().strip('?'):
            listMods(chan, modList, ircs)
        elif "how do you feel about" in command.lower().strip('?'):
            tellYourFeels(command, chan, ircs)
        elif "go fight" in command:
            fightSomething(command, chan, ircs)
        elif "give" in command.lower() and "awful point" in command.lower():
            giveAwfulPoints(command, chan, user, ircs)
        elif "how many awful points does" in command.lower():
            getUserAwfulPoints(command, chan, ircs)
        elif "show me the awful scores" in command.lower():
            listAwfulScores(user, ircs)
        elif "who is everyone" in command.lower():
            list_all_pagans(user, ircs)
        elif "what type of pagan is" in command.lower() or "what kind of pagan is" in command.lower() or "what sort of pagan is" in command.lower() or "who is" in command.lower() or "what is" in command.lower():
            retrievePaganType(command, chan, ircs)
        #elif re.match('^((?!who)\S+) is (.+)', command.strip(), flags=re.IGNORECASE):
        elif "is" in command.lower():
            assignPaganType(command, chan, ircs)
        ##        elif "who are the" in command.lower():
##            retrievePagansOfType(command, chan, ircs)
        elif "www" in command.lower() or "http" in command.lower():
            findUrlTitle(command, chan, ircs)
        elif "tell" in command.lower():
            tellUser(command, user, chan, ircs)
        elif "roll" in command.lower():
            rollDice(command, user, chan, ircs)
        elif (command.strip() == 'die' or command.strip() == 'stop' or command.strip() == 'quit' or command.strip() == 'kill') and (user in modList):
            sys.exit()
        else:
            sendChanMsg(chan, user + ", you're wrong, go read some lore.", ircs)


nickString = "NICK " + botnick + "\r\n"
userString = "USER " + botnick + " " + botnick + " " + botnick + " :Pagan Bot for #Pagan\r\n"
data = ""
logMsg(userString)
logMsg(nickString)
ircsock = socket.socket()
ircsock.connect((server, 6667))
ircsock.send(userString.encode('utf-8'))
ircsock.send(nickString.encode('utf-8'))
joinChan(channel, ircsock)
while 1:
    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip(('\r\n').encode('utf-8'))
    logMsg(ircmsg)
    message = ''
    user, chan, command = "","",""
    try:
        message = ircmsg.decode('utf-8')
    except:
        sendChanMsg(channel, "What kinda weird shit did you just say?", ircsock)
    if "PING :" in message:
        pingData = message.strip("PING :")
        logMsg(pingData)
        ping(pingData, ircsock)
    if "esper.net 001" in message:
        ircsock.send(userString.encode('utf-8'))
        ircsock.send(nickString.encode('utf-8'))
        ircsock.send(('PRIVMSG NickServ :IDENTIFY HeathenBot1\r\n').encode('utf-8'))
        joinChan(channel, ircsock)
    else:
        try:
            (user,chan,command)=decomposeMsg(message)
        except Exception as err:
            if str(err)!= ("list index out of range"):
                logMsg(str(err))
        if "join" in message.lower():
            retrieveMessage(chan, user, ircsock)
        elif ("www." in command or "http" in command) and (chan.lower()==channel.lower()):
            runCommand(user, chan, command, ircsock)
        elif(chan.lower()==channel.lower() and command[0:len(botnick)].lower()==botnick.lower()):
            runCommand(user, chan, command, ircsock)
        elif (chan.lower()==botnick.lower()) and (user.lower()!="nickserv") and (" " not in user):
            runCommand(user, chan, command, ircsock)
