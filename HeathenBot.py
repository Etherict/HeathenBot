import socket
import logging
import sys
import time
import random
import re
import operator
import csv
import datetime
from HeathenBotFunctions import *

server = "irc.esper.net"
channel = "#pagan"
botnick  = "HeathenBot"
modList = ['Etherict','hrafnblod','UsurpedLettuce','RyderHiME','HereticHierophant','manimatr0n','Anarcho-Transhuman','c_brighde','cmacis','MidDipper', 'EINARR_THE_BERSERKER']
awfulReader = csv.reader(open('awfulPoints.csv', 'r'))
awfulPoints = dict(x for x in awfulReader)
awfulPoints = dict((k,int(v)) for k,v in awfulPoints.items())
paganReader = csv.reader(open('paganTypes.csv', 'r'))
paganTypes = dict(x for x in paganReader)    

#refusing to "commandTree" because fuck trees.
def commandSmallShrub(ircData, chan, listOfMods, ircs):
    logMsg(ircData)
    ircData = ircData.split(':')
    user = ircData[1].split('!')[0]
    ircData = ircData[-1].split(',')
    command = ircData[-1]
    command = command.strip('.').strip()
    logMsg("Command received: " + command)
    logMsg('USER parsed as ' + user)
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
            sendHelpToUser(user, listOfMods, ircs)
        elif "who's a mod" in command.lower().strip('?'):
            listMods(chan, listOfMods, ircs)
        elif "how do you feel about" in command.lower().strip('?'):
            tellYourFeels(command, chan, ircs)
        elif "go fight" in command:
            fightSomething(command, chan, ircs)
        elif "give" in command.lower() and "awful point" in command.lower():
            awfulPoints = giveAwfulPoints(command, chan, user, awfulPoints, ircs)
        elif "how many awful points does" in command.lower():
            getUserAwfulPoints(command, chan, awfulPoints, ircs)
        elif "show me the awful scores" in command.lower():
            listAwfulScores(awfulPoints, chan, awfulPoints, ircs)
        elif "is a" in command.lower():
            paganTypes = assignPaganType(command, chan, paganTypes, ircs)
        elif "what type of pagan is" in command.lower() or "what kind of pagan is" in command.lower() or "what sort of pagan is" in command.lower() or "who is" in command.lower():
            retrievePaganType(command, chan, paganTypes, ircs)
        elif (command.strip() == 'die' or command.strip() == 'stop' or command.strip() == 'quit' or command.strip() == 'kill') and (user in listOfMods):
            sys.exit()
        else:
            sendChanMsg(channel, user + ", you're wrong, go read some lore.", ircs)


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
    if "heathenbot," in message.lower() or "heathenbot:" in message.lower():
        try:
            commandSmallShrub(message, channel, modList, ircsock)
        except SystemExit:
            saveDictToFile('awfulpoints.csv', awfulPoints)
            saveDictToFile('paganTypes.csv', paganTypes)
            logMsg(sys.exc_info())
            sys.exit()
        except:
            sendChanMsg(channel, "Good job, you broke me. Dumbass.", ircsock)
            logMsg(sys.exc_info())
