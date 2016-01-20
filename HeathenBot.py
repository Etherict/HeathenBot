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

def commandTree(ircData, chan, listOfMods, ircs):
    logMsg(ircData)
    ircData = ircData.split(':')
    chan = ircData[1].split(' ')[2]
    user = ircData[1].split('!')[0]
    ircData = ircData[-1].split(',')
    command = ircData[-1]
    command = command.strip('.').strip()
    logMsg("Command received: " + command)
    logMsg('USER parsed as ' + user)
    #logMsg('Chan parsed as ' + chan)
    if chan == 'HeathenBot':
        chan = user

    if user != 'HeathenBot':
        if "convert" in command.lower():
            convertTemperatures(command, chan, ircs)
        elif "google" in command.lower():
            google(command, chan, user, ircs)
        elif "give me a hammer" in command.lower():
            giveHammer(chan, ircs)
        elif "cheers" in command.lower():
            raiseCheers(chan, ircs)
        elif "sing me a song" in command.lower():            
            singSong(chan, ircs)
        elif "be quiet" in command.lower() and user in listOfMods:
            muteBot(command)
        elif "help" in command.lower():
            sendHelpToUser(user, chan, listOfMods, ircs)
        elif "who's a mod" in command.lower().strip('?'):
            listMods(chan, listOfMods, ircs)
        elif "how do you feel about" in command.lower().strip('?'):
            tellYourFeels(command, chan, ircs)
        elif "go fight" in command:
            fightSomething(command, chan, ircs)
        elif "give" in command.lower() and "awful point" in command.lower():
            giveAwfulPoints(command, chan, user, ircs)
        elif "how many awful points does" in command.lower():
            getUserAwfulPoints(command, chan, ircs)
        elif "show me the awful scores" in command.lower():
            listAwfulScores(chan, ircs)
        elif re.match('^((?!who)\S+) is (.+)', command.strip(), flags=re.IGNORECASE):
            paganTypes = assignPaganType(command, chan, ircs)
        elif "what type of pagan is" in command.lower() or "what kind of pagan is" in command.lower() or "what sort of pagan is" in command.lower() or "who is" in command.lower() or "what is" in command.lower():
            retrievePaganType(command, chan, ircs)
##        elif "who are the" in command.lower():
##            retrievePagansOfType(command, chan, ircs)
        elif (command.strip() == 'die' or command.strip() == 'stop' or command.strip() == 'quit' or command.strip() == 'kill') and (user in listOfMods):
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
    print(ircmsg)
    message = ''
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
    if "PRIVMSG" in message and not "#" in message and not(botnick.lower() + "," in message.lower() or botnick.lower() + ":" in message.lower()):
        message = botnick + ", " + message
    if botnick.lower() + "," in message.lower() or botnick.lower() + ":" in message.lower():
        try:
            commandTree(message, channel, modList, ircsock)
        except SystemExit:
            close_database()
            logMsg(sys.exc_info())
            sys.exit()
        except:
            sendChanMsg(channel, "Good job, you broke me. Dumbass.", ircsock)
            logMsg(sys.exc_info())
