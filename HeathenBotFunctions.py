import socket
import logging
import sys
import time
import random
import re
import operator
import csv
import datetime

from pagan_database import *
from IRC_functions import *


    
#Convert temperatures    
def convertFahrenheitToCelsius(tempToConvert, chan, ircs):
    message = tempToConvert + "F is " + str(round((float(tempToConvert) - 32)/1.8)) + "C. . .What, are you stupid?"
    sendChanMsg(chan, message, ircs)

def convertFahrenheitToKelvin(tempToConvert, chan, ircs):
    message = tempToConvert + "F is " + str(round(((float(tempToConvert) - 32)/1.8) + 273.15)) + "K. . .really?"
    sendChanMsg(chan, message, ircs)

def convertCelsiusToFahrenheit(tempToConvert, chan, ircs):
    message = tempToConvert + "C is " + str(round(float(tempToConvert) * 1.8 + 32)) + "F. . . Couldn't you have done that yourself?"
    sendChanMsg(chan, message, ircs)

def convertCelsiusToKelvin(tempToConvert, chan, ircs):
    message = tempToConvert + "C is " + str(round(float(tempToConvert) + 273.15)) + "K. . .c'mon, it's just freakin' addition."
    sendChanMsg(chan, message, ircs)

def convertKelvinToFahrenheit(tempToConvert, chan, ircs):
    message = tempToConvert + "K is " + str(round((float(tempToConvert) - 273.15) * 1.8 + 32)) + "F. . .Seriously, did you drop out or something?"
    sendChanMsg(chan, message, ircs)

def convertKelvinToCelsius(tempToConvert, chan, ircs):
    message = tempToConvert + "K is " + str(round(float(tempToConvert) - 273.15)) + "C. . .Read a book."
    sendChanMsg(chan, message, ircs)

def convertTemperatures(command, chan, ircs):
    tempToConvert = command.split(' ')[-1].lower()
    if tempToConvert.find('fc') != -1:
        tempToConvert = tempToConvert.strip('fc')
        convertFahrenheitToCelsius(tempToConvert, chan, ircs)
    elif tempToConvert.find('fk') != -1:
        tempToConvert = tempToConvert.strip('fk')
        convertFahrenheitToKelvin(tempToConvert, chan, ircs)
    elif tempToConvert.find('cf') != -1:
        tempToConvert = tempToConvert.strip('cf')
        convertCelsiusToFahrenheit(tempToConvert, chan, ircs)
    elif tempToConvert.find('ck') != -1:
        tempToConvert = tempToConvert.strip('ck')
        convertCelsiusToKelvin(tempToConvert, chan, ircs)
    elif tempToConvert.find('kf') != -1:
        tempToConvert = tempToConvert.strip('kf')
        convertKelvinToFahrenheit(tempToConvert, chan, ircs)
    elif tempToConvert.find('kc') != -1:
        tempToConvert = tempToConvert.strip('kc')
        convertKelvinToCelsius(tempToConvert, chan, ircs)
    else:
        sendChanMsg(chan, "I'm sorry, I don't understand. Have you tried not being stupid?")
        
def google(command, chan, user, ircs):
    termToLMGTFY = command.lower().replace('google ', "").replace(' ', '%20')
    sendChanMsg(chan, "Here you go, " + user + ", I did this incredibly difficult task for you: http://www.lmgtfy.com/?q=" + termToLMGTFY, ircs)

def giveHammer(chan, ircs):
    sendChanMsg(chan, "           .-----,           ", ircs)
    sendChanMsg(chan, "           |-----|           ", ircs)
    sendChanMsg(chan, "           |-----|           ", ircs)
    sendChanMsg(chan, "           .-----,           ", ircs)
    sendChanMsg(chan, "            |-|-|            ", ircs)
    sendChanMsg(chan, "            |-|-|            ", ircs)
    sendChanMsg(chan, "            |-|-|            ", ircs)
    sendChanMsg(chan, "           |-----|           ", ircs)
    sendChanMsg(chan, "          |-------|          ", ircs)
    sendChanMsg(chan, "        |-----------|        ", ircs)
    sendChanMsg(chan, "  |-----------------------|  ", ircs)
    sendChanMsg(chan, "  |-----------------------|  ", ircs)
    sendChanMsg(chan, "  |-----------------------|  ", ircs)
    sendChanMsg(chan, "  |-----------------------|  ", ircs)
    sendChanMsg(chan, "             |_|             ", ircs)

def raiseCheers(chan, ircs):
    numberToSelect = random.randint(0, 8)
    if numberToSelect == 1:
        sendChanMsg(chan, "Here's to Hell! May my stay there be as much fun as my way there!", ircs)
    if numberToSelect == 2:
        sendChanMsg(chan, "One shot, two shots, three shots, four...if she's ugly we'll have 4 more.", ircs)
    if numberToSelect == 3:
        sendChanMsg(chan, "Here's to honor...hitting honor, getting honor, staying honor...and if you can't come in her...come honor.", ircs)
    if numberToSelect == 4:
        sendChanMsg(chan, "Here's to those who love us terribly. May they soon improve.", ircs)
    if numberToSelect == 5:
        sendChanMsg(chan, "Time is never wasted when you're wasted all the time.", ircs)
    if numberToSelect == 6:
        sendChanMsg(chan, "I don't have a drinking problem. I drink, I get drunk, I fall over...no problem.", ircs) 
    if numberToSelect == 7:              
        sendChanMsg(chan, "Take everything in moderation, especially moderation.", ircs)

def singSong(chan, ircs):
	songs = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"
		,"https://www.youtube.com/watch?v=sdc0ZU0YRe4"
		,"https://www.youtube.com/watch?v=fu2bgwcv43o"
		,"https://www.youtube.com/watch?v=6NXnxTNIWkc"
		,"https://www.youtube.com/watch?v=XxYJmfjVwqA"
		,"https://www.youtube.com/watch?v=xlUAjtduiqg"
		,"https://www.youtube.com/watch?v=UB8Qx_Hce1s"
		,"https://www.youtube.com/watch?v=J599h8ADmRI"
		,"https://www.youtube.com/watch?v=mKNIHaBCkcw"
		,"https://www.youtube.com/watch?v=jAukGWuVyEo"
		,"https://www.youtube.com/watch?v=qw2-gbsMy7k"
		,"https://www.youtube.com/watch?v=jsdawgd0azk"
		,"https://www.youtube.com/watch?v=aSz1eZXpMKY"
	]
	numberToSelect = random.randint(-1, len(songs))
	sendChanMsg(chan, songs[numberToSelect], ircs)
	
##def saveDictToFile(fileName, dictToSave):
##    fileWriter = csv.writer(open(fileName, 'w', newline=''))
##    for dictKey, dictValue in dictToSave.items():
##        fileWriter.writerow([dictKey, dictValue])

def muteBot(command):
    periodToMute = command.split(' ')[-1]
    if periodToMute.lower().find('s') != -1:
        periodToMute = float(periodToMute.lower().strip('s'))
        mute(periodToMute)
    else:
        mute(float(periodToMute * 60))

def sendHelpToUser(user, chan, listOfMods, ircs):
    sendChanMsg(chan, user + ' is an ergi who needs help!', ircs)
    sendChanMsg(user, "List of commands is as follows:\r\n", ircs)
    sendChanMsg(user, "Convert <number>FC, Convert Fahrenheit to Celsius.\r\n", ircs)
    sendChanMsg(user, "Convert <number>FK, Convert Fahrenheit to Kelvin.\r\n", ircs)
    sendChanMsg(user, "Convert <number>CF, Convert Celsius to Fahrenheit.\r\n", ircs)
    sendChanMsg(user, "Convert <number>CK, Convert Celsius to Kelvin.\r\n", ircs)
    sendChanMsg(user, "Convert <number>KF, Convert Kelvin to Fahrenheit.\r\n", ircs)
    sendChanMsg(user, "Convert <number>KC, Convert Kelvin to Celsius.\r\n", ircs)
    sendChanMsg(user, "Google <Search terms>, Runs a Google search. . .maybe.\r\n", ircs)
    if user in listOfMods:
        sendChanMsg(user, "Be Quiet <number>, I'll shut up for <number> minutes. Be careful, I won't respond to pings either, so this might kill me. (Mods/bot owner only)\r\n", ircs)
        sendChanMsg(user, "Be Quiet <number>s, I'll shut up for <number> seconds. Same deal as with minutes, if I'm quiet for too long, the server will kill me.\r\n", ircs)
        sendChanMsg(user, "Kill, Please don't do this, it hurts me. . .(Mods/bot owner only)\r\n", ircs)
        sendChanMsg(user, "Stop, Same as Kill.", ircs)

def listMods(chan, listOfMods, ircs):
    for mod in listOfMods:
        sendChanMsg(chan, mod, ircs)

def tellYourFeels(command, chan, ircs):
    pattern = re.compile("how do you feel about", re.IGNORECASE)
    termToFuck = command.strip('?')
    termToFuck = pattern.sub("", termToFuck).strip()
    sendChanMsg(chan, "Fuck " + termToFuck, ircs)

def fightSomething(command, chan, ircs):
    pattern = re.compile("go fight (a?n? ?)", re.IGNORECASE)
    termToFight = command.replace('.', '')
    termToFight = pattern.sub("", termToFight).strip()
    sendChanMsg(chan, termToFight + ", you are a nithing, I challenge you to holmgang! On an island! With tigers!", ircs)

def giveAwfulPoints(command, chan, user, ircs):
    pointee = command.split(" ")[1]
    points = float(command.split(" ")[2])
    give_awfulpoints(pointee, points, chan, ircs)
    
    sendChanMsg(chan, user + " has given " + pointee + " " + str(points) + " awful points!", ircs)
    get_awfulpoints(pointee, chan, ircs)

def getUserAwfulPoints(command, chan, ircs):
    pointee = command.split(" ")[5]
    get_awfulpoints(pointee, chan, ircs)

def listAwfulScores(chan, ircs):
    get_all_awfulpoints(chan, ircs)

def assignPaganType(command, chan, ircs):
    splitCommand = command.split(" ")
    personInQuestion = splitCommand[0]
    paganType = ""
    for i in range(2, len(splitCommand)):
        paganType += splitCommand[i] + " "
    if "heathen" in paganType.lower():
        sendChanMsg(chan, "Excellent, all is well.", ircs)
    else:
        sendChanMsg(chan, personInQuestion + " is wrong.", ircs)
    paganType = paganType.strip()
    create_wight(personInQuestion, paganType)
    

def retrievePaganType(command, chan,ircs):
    personInQuestion = command.strip("?").split(" ")[-1]
    get_pagan(personInQuestion, chan,ircs)

def retrievePagansOfType(command, chan, ircs):
    list_pagantype(command[-1], chan, ircs)
