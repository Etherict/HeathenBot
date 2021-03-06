import sqlite3 as sql

from IRC_functions import *

conn = sql.connect('pagantypes.db')

c = conn.cursor()

def create_table_pagans():
  c.execute("CREATE TABLE pagans (Name VARCHAR, Definition VARCHAR, AwfulPoints FLOAT)")

def create_table_messages():
  c.execute("CREATE TABLE messages (Sender VARCHAR, Receiver VARCHAR, Message VARCHAR)")

def create_wight(name, definition):
  rows = c.execute("SELECT * FROM pagans WHERE Name = ?", [name])
  if next(rows,None) == None:
    c.execute("INSERT INTO pagans (Name, Definition, AwfulPoints) VALUES(?,?,?)", [name, definition, 0])
  else:
    c.execute("UPDATE pagans SET Definition = ? WHERE Name = ?", [definition, name])
  conn.commit()

def dump_database():
  s = "SELECT * FROM pagans"
  for row in c.execute(s):
    sendChanMsg(chan, row, ircs)

def list_all_pagans(chan, ircs):
  s=("SELECT * FROM pagans")
  for row in c.execute(s):
    sendChanMsg(chan, row[0] + " is " + row[1], ircs)

def list_pagantype(definition, chan, ircs):
  s = "SELECT * FROM pagans"
  for row in c.execute(s):
    if (definition.lower() in row[1].lower()):
      sendChanMsg(chan, row[0] + " is a " + row[1], ircs)

def get_pagan(name, chan, ircs):
  c.execute("SELECT Definition FROM pagans WHERE Name = ?",[name])
  try:
    sendChanMsg(chan, name +" is "+c.fetchone()[0], ircs)
  except:
    sendChanMsg(chan, name+" is not a registered pagan. Probably a filthy eclectic.", ircs)
    
def get_awfulpoints(name, chan, ircs):
  c.execute("SELECT AwfulPoints FROM pagans WHERE Name = ?",[name])
  try:
    sendChanMsg(chan, name + " has "+str(c.fetchone()[0])+" awful points", ircs)
  except:
    sendChanMsg(chan, name+" is not a registered pagan. Please register them, so you can tell us how awful they are!", ircs)

def get_all_awfulpoints(chan, ircs):
    rows=c.execute("SELECT Name, Awfulpoints FROM pagans")
    for row in rows:
        msg = row[0] + " : " + str(row[1])
        sendChanMsg(chan, msg, ircs)
    
def give_awfulpoints(name, points, chan, ircs, trycount = 0):
  rows=c.execute("SELECT AwfulPoints FROM pagans WHERE Name = ?",[name])
  try: 
    points+=rows.fetchone()[0]
    c.execute("UPDATE  pagans SET AwfulPoints = ? WHERE Name = ?", [points, name])
    conn.commit()
  except:
    if(trycount < 1):
        create_wight(name, "an unregistered pagan")
        give_awfulpoints(name, points, chan, ircs, 1)
    else:
        sendChanMsg(chan, "I can't do it.", ircs)

def remove_wight(name, chan, ircs):
  try:
    c.execute("DELETE FROM pagans WHERE Name = ?", [name])
    conn.commit()
  except:
    sendChanMsg(chan, "Tried to remove a non-existent wight", ircs)

def close_database():
  conn.commit()
  conn.close()

def retrieveMessage(chan, user, ircs):
    rows = c.execute("Select * from messages where Receiver =?",[user])
    for r in rows:
      sender = r[0]
      message = r[2]
      sendChanMsg(chan, sender + " said: " + message, ircs)
    c.execute("DELETE FROM messages where Receiver = ?",[user])
    conn.commit()

def storeMessage(sender, receiver, msg, ircs):
  c.execute("INSERT INTO messages (Sender, Receiver, Message) VALUES(?,?,?)",[sender, receiver, msg])
  conn.commit()

  
try:
    create_table_pagans()
    logMsg("Created table Pagans")
except:
    logMsg("Pagans exists")

try:
  create_table_messages()
  logMsg("Created table Messages")
except:
  logMsg("Table Messages exists")
