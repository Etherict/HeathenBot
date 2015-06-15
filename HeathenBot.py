import socket
import logging
import sys
import time
import random
import re
import operator
import csv

server = "irc.esper.net"
channel = "#pagan"
botnick  = "HeathenBot"
modList = ['Etherict','hrafnblod','UsurpedLettuce','RyderHiME','HereticHierophant','manimatr0n','Anarcho-Transhuman','c_brighde','cmacis','MidDipper', 'EINARR_THE_BERSERKER']
reader = csv.reader(open('awfulPoints.csv', 'r'))
awfulPoints = dict(x for x in reader)
awfulPoints = dict((k,int(v)) for k,v in awfulPoints.items())

#respond to server pings
def ping(pingData):
    pong = "PONG :" + pingData
    logging.info(pong)
    ircsock.send(pong.encode('utf-8'))

#send private message
def sendChanMsg(chan, msg):
    logging.info("Sending message: " + msg)
    ircsock.send(("PRIVMSG " + chan + " :" + msg + "\r\n").encode('utf-8'))

#join a channel
def joinChan(chan):
    ircsock.send(("JOIN " + chan + "\r\n").encode('utf-8'))

def mute(periodToMute):
    time.sleep(periodToMute)
    
#Convert temperatures    
def convertFahrenheitToCelsius(tempToConvert, chan):
    message = tempToConvert + "F is " + str(round((float(tempToConvert) - 32)/1.8)) + "C. . .What, are you stupid?"
    sendChanMsg(chan, message)

def convertFahrenheitToKelvin(tempToConvert, chan):
    message = tempToConvert + "F is " + str(round(((float(tempToConvert) - 32)/1.8) + 273.15)) + "K. . .really?"
    sendChanMsg(chan, message)

def convertCelsiusToFahrenheit(tempToConvert, chan):
    message = tempToConvert + "C is " + str(round(float(tempToConvert) * 1.8 + 32)) + "F. . . Couldn't you have done that yourself?"
    sendChanMsg(chan, message)

def convertCelsiusToKelvin(tempToConvert, chan):
    message = tempToConvert + "C is " + str(round(float(tempToConvert) + 273.15)) + "K. . .c'mon, it's just freakin' addition."
    sendChanMsg(chan, message)

def convertKelvinToFahrenheit(tempToConvert, chan):
    message = tempToConvert + "K is " + str(round((float(tempToConvert) - 273.15) * 1.8 + 32)) + "F. . .Seriously, did you drop out or something?"
    sendChanMsg(chan, message)

def convertKelvinToCelsius(tempToConvert, chan):
    message = tempToConvert + "K is " + str(round(float(tempToConvert) - 273.15)) + "C. . .Read a book."
    sendChanMsg(chan, message)

#refusing to "commandTree" because fuck trees.
def commandSmallShrub(ircData):
    logging.info(ircData)
    ircData = ircData.split(':')
    user = ircData[1].split('!')[0]
    ircData = ircData[-1].split(',')
    command = ircData[-1]
    command = command.strip('.').strip()
    logging.info("Command received: " + command)
    logging.info('USER parsed as ' + user)
    if user != 'HeathenBot':
        if "convert" in command.lower():
            tempToConvert = command.split(' ')[-1].lower()
            if tempToConvert.find('fc') != -1:
                tempToConvert = tempToConvert.strip('fc')
                convertFahrenheitToCelsius(tempToConvert, channel)
            elif tempToConvert.find('fk') != -1:
                tempToConvert = tempToConvert.strip('fk')
                convertFahrenheitToKelvin(tempToConvert, channel)
            elif tempToConvert.find('cf') != -1:
                tempToConvert = tempToConvert.strip('cf')
                convertCelsiusToFahrenheit(tempToConvert, channel)
            elif tempToConvert.find('ck') != -1:
                tempToConvert = tempToConvert.strip('ck')
                convertCelsiusToKelvin(tempToConvert, channel)
            elif tempToConvert.find('kf') != -1:
                tempToConvert = tempToConvert.strip('kf')
                convertKelvinToFahrenheit(tempToConvert, channel)
            elif tempToConvert.find('kc') != -1:
                tempToConvert = tempToConvert.strip('kc')
                convertKelvinToCelsius(tempToConvert, channel)
            else:
                sendChanMsg(channel, "I'm sorry, I don't understand. Have you tried not being stupid?")
        elif "google" in command.lower():
            termToLMGTFY = command.lower().replace('google ', "").replace(' ', '%20')
            sendChanMsg(channel, "Here you go, " + user + ", I did this incredibly difficult task for you: http://www.lmgtfy.com/?q=" + termToLMGTFY)
        elif "give me a hammer" in command.lower():
            sendChanMsg(channel, "           .-----,           ")
            sendChanMsg(channel, "           |-----|           ")
            sendChanMsg(channel, "           |-----|           ")
            sendChanMsg(channel, "           .-----,           ")
            sendChanMsg(channel, "            |-|-|            ")
            sendChanMsg(channel, "            |-|-|            ")
            sendChanMsg(channel, "            |-|-|            ")
            sendChanMsg(channel, "           |-----|           ")
            sendChanMsg(channel, "          |-------|          ")
            sendChanMsg(channel, "        |-----------|        ")
            sendChanMsg(channel, "  |-----------------------|  ")
            sendChanMsg(channel, "  |-----------------------|  ")
            sendChanMsg(channel, "  |-----------------------|  ")
            sendChanMsg(channel, "  |-----------------------|  ")
            sendChanMsg(channel, "             |_|             ")
            
        elif "cheers" in command.lower():
            numberToSelect = random.randint(0, 8)
            if numberToSelect == 1:
                sendChanMsg(channel, "Here’s to Hell! May my stay there be as much fun as my way there!")
            if numberToSelect == 2:
                sendChanMsg(channel, "One shot, two shots, three shots, four...if she's ugly we'll have 4 more.")
            if numberToSelect == 3:
                sendChanMsg(channel, "Here’s to honor…hitting honor, getting honor, staying honor…and if you can’t come in her… come honor.")
            if numberToSelect == 4:
                sendChanMsg(channel, "Here's to those who love us terribly. May they soon improve.")
            if numberToSelect == 5:
                sendChanMsg(channel, "Time is never wasted when you're wasted all the time.")
            if numberToSelect == 6:
                sendChanMsg(channel, "I don't have a drinking problem. I drink, I get drunk, I fall over...no problem.") 
            if numberToSelect == 7:              
                sendChanMsg(channel, "Take everything in moderation, especially moderation.") 
                
        elif "sing me a song" in command.lower():
            numberToSelect = random.randint(0, 8)
            if numberToSelect == 1:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            elif numberToSelect == 2:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=sdc0ZU0YRe4")
            elif numberToSelect == 3:
                 sendChanMsg(channel, "https://www.youtube.com/watch?v=fu2bgwcv43o")
            elif numberToSelect == 4:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=6NXnxTNIWkc")
            elif numberToSelect == 5:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=XxYJmfjVwqA")
            elif numberToSelect == 6:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=xlUAjtduiqg")
            elif numberToSelect == 7:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=UB8Qx_Hce1s")
            elif numberToSelect == 8:
                sendChanMsg(channel, "https://www.youtube.com/watch?v=2PhLze0fjDQ")
        elif "show me some bullshit" in command.lower():
            sendChanMsg(channel, "http://romandruid.blogspot.com/?m=0")
        elif "be quiet" in command.lower() and user in modList:
            periodToMute = command.split(' ')[-1]
            if periodToMute.lower().find('s') != -1:
                periodToMute = float(periodToMute.lower().strip('s'))
                mute(periodToMute)
            else:
                mute(float(periodToMute * 60))
        elif "rickroll" in command.lower():
            sendChanMsg(channel, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        elif "help" in command.lower():
            sendChanMsg(channel, user + ' is an ergi who needs help!')
            sendChanMsg(user, "List of commands is as follows:\r\n")
            sendChanMsg(user, "Convert <number>FC, Convert Fahrenheit to Celsius.\r\n")
            sendChanMsg(user, "Convert <number>FK, Convert Fahrenheit to Kelvin.\r\n")
            sendChanMsg(user, "Convert <number>CF, Convert Celsius to Fahrenheit.\r\n")
            sendChanMsg(user, "Convert <number>CK, Convert Celsius to Kelvin.\r\n")
            sendChanMsg(user, "Convert <number>KF, Convert Kelvin to Fahrenheit.\r\n")
            sendChanMsg(user, "Convert <number>KC, Convert Kelvin to Celsius.\r\n")
            sendChanMsg(user, "Google <Search terms>, Runs a Google search. . .maybe.\r\n")
            if user in modList:
                sendChanMsg(user, "Be Quiet <number>, I'll shut up for <number> minutes. Be careful, I won't respond to pings either, so this might kill me. (Mods/bot owner only)\r\n")
                sendChanMsg(user, "Be Quiet <number>s, I'll shut up for <number> seconds. Same deal as with minutes, if I'm quiet for too long, the server will kill me.\r\n")
                sendChanMsg(user, "Kill, Please don't do this, it hurts me. . .(Mods/bot owner only)\r\n")
                sendChanMsg(user, "Stop, Same as Kill.")
        elif "who's a mod" in command.lower().strip('?'):
            for mod in modList:
                sendChanMsg(channel, mod)
        elif "how do you feel about" in command.lower().strip('?'):
            pattern = re.compile("how do you feel about", re.IGNORECASE)
            termToFuck = command.strip('?')
            termToFuck = pattern.sub("", termToFuck).strip()
            sendChanMsg(channel, "Fuck " + termToFuck)
        elif "go fight" in command:
            pattern = re.compile("go fight (an? )", re.IGNORECASE)
            termToFight = command.replace('.', '')
            termToFight = pattern.sub("", termToFight).strip()
            sendChanMsg(channel, termToFight + ", you are a nithing, I challenge you to holmgang! On an island! With tigers!")
        elif "give" in command.lower() and "awful point" in command.lower():
            pointee = command.split(" ")[1]
            points = int(command.split(" ")[2])
            if pointee in awfulPoints:
                awfulPoints[pointee] = awfulPoints[pointee] + points                
            else:
                awfulPoints[pointee] = points
            sendChanMsg(channel, pointee + " now has " + str(awfulPoints[pointee]) + " awful points!")
        elif "how many awful points does" in command.lower():
            pointee = command.split(" ")[5]
            if pointee in awfulPoints:
                points = awfulPoints[pointee]
            else:
                points = 0
            sendChanMsg(channel, pointee + " has " + str(points) + " awful points!")
        elif "show me the awful scores" in command.lower():
            sortedScores = sorted(awfulPoints.items(), key=operator.itemgetter(1))
            sortedScores.reverse()
            sendChanMsg(channel, "Scoreboard:")
            for user, score in sortedScores:
                sendChanMsg(channel, user + ": " + str(score))
        elif (command.strip() == 'die' or command.strip() == 'stop' or command.strip() == 'quit' or command.strip() == 'kill') and (user in modList):
            writer = csv.writer(open('awfulPoints.csv', 'w', newline=''))
            for user, score in awfulPoints.items():
                writer.writerow([user, score])
            sys.exit()
        else:
            sendChanMsg(channel, user + ", you're wrong, go read some lore.")

logging.basicConfig(filename='log.log',level=logging.INFO)
nickString = "NICK " + botnick + "\r\n"
userString = "USER " + botnick + " " + botnick + " " + botnick + " :Pagan Bot for #Pagan\r\n"
data = ""
logging.info(userString)
logging.info(nickString)
ircsock = socket.socket()
ircsock.connect((server, 6667))
ircsock.send(userString.encode('utf-8'))
ircsock.send(nickString.encode('utf-8'))
joinChan(channel)
while 1:
    ircmsg = ircsock.recv(2048)
    ircmsg = ircmsg.strip(('\r\n').encode('utf-8'))
    logging.info(ircmsg)
    print(ircmsg)
    message = ''
    try:
        message = ircmsg.decode('utf-8')
    except:
        sendChanMsg(channel, "What kinda weird shit did you just say?")
    if "PING :" in message:
        pingData = message.strip("PING :")
        logging.info(pingData)
        ping(pingData)
    if "esper.net 001" in message:
        ircsock.send(userString.encode('utf-8'))
        ircsock.send(nickString.encode('utf-8'))
        ircsock.send(('PRIVMSG NickServ :IDENTIFY HeathenBot1\r\n').encode('utf-8'))
        joinChan(channel)
    if "heathenbot," in message.lower():
        try:
            commandSmallShrub(message)
        except SystemExit:            
            logging.info(sys.exc_info())
            sys.exit()
        except:
            sendChanMsg(channel, "Good job, you broke me. Dumbass.")
            logging.info(sys.exc_info())
