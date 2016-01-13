import sqlite3 as sql

from IRC_functions import *

conn = sql.connect('pagantypes.db')

c = conn.cursor()

def create_table():
  c.execute("CREATE TABLE pagans (Name VARCHAR, Definition VARCHAR, AwfulPoints FLOAT)")

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

def list_pagantype(definition, chan, ircs):
  s = "SELECT * FROM pagans"
  for row in c.execute(s):
    if (definition.lower() in row[1].lower()):
      sendChanMsg(chan, row[0] + " is a " + row[1], ircs)

def get_pagan(name, chan, ircs):
  c.execute("SELECT Definition FROM pagans WHERE Name = ?",[name])
  try:
    sendChanMsg(chan, name +" is a "+c.fetchone()[0], ircs)
  except:
    sendChanMsg(chan, name+" does not seem to exist", ircs)
    
def get_awfulpoints(name, chan, ircs):
  c.execute("SELECT AwfulPoints FROM pagans WHERE Name = ?",[name])
  try:
    sendChanMsg(chan, name + " has "+str(c.fetchone()[0])+" awful points", ircs)
  except:
    sendChanMsg(chan, name+" does not seem to exist", ircs)

def get_all_awfulpoints(chan, ircs):
    rows=c.execute("SELECT Name, Awfulpoints FROM pagans")
    for row in rows:
        sendChanMsg(chan, row, ircs)
    
def give_awfulpoints(name, points, chan, ircs):
  rows=c.execute("SELECT AwfulPoints FROM pagans WHERE Name = ?",[name])
  try: 
    points+=rows.fetchone()[0]
    c.execute("UPDATE  pagans SET AwfulPoints = ? WHERE Name = ?", [points, name])
    conn.commit()
  except:
    sendChanMsg(chan, "Tried to update AwfulPoints of a non-existent Wight", ircs)

def remove_wight(name, chan, ircs):
  try:
    c.execute("DELETE FROM pagans WHERE Name = ?", [name])
    conn.commit()
  except:
    sendChanMsg(chan, "Tried to remove a non-existent wight", ircs)
def close_database():
  conn.close()

try:
    create_database()
    logMsg("Created Database")
except:
    logMsg("Database exists")