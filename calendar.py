import time
import datetime
import json
import sys
import os

class Entry():
    def __init__(self, participants=None, name = None, day=None, start=None, end=None):
        self.participants = participants
        self.name = name
        self.day = day
        self.start = start
    self.end = end

    def __repr__(self):
        return "Participants: %s, Name: %s, Day: %s, Time: %s - %s" % (self.participants, self.name, self.day, self.start, self.end)
    def __eq__(self, other):
        if isinstance(other, Entry):
            return ((self.participants == other.participants) and (self.name == other.name) and (self.day == other.day) and (self.start == other.start) and (self.end == other.end))
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)

    @staticmethod
    def load(js):
        a = Entry()
        a.__dict__ = js
        return a
from event import Event

class EntrySet():
    def __init__(self):
        self.calendar = []

    def __repr__(self):
        strs = map(str, self.calendar)
        for i in xrange(0, len(strs)):
            strs[i] = "[" + str(i) + "] " + strs[i]
        return '\n'.join(strs)

    def __getitem__(self, key):
        return self.calendar[key]

    #log file exists with entries
    def create_from_log(self, node):
        node.log.close()
        log =  open('log.dat','r')
        for l in log:
            event = json.loads(l)
            event = Event.load(event)
            event.entry = Entry.load(event.entry)
            event.apply(node.entry_set, node)
            node.events.append(event)
            for i in event.entry.participants:
                if event.time > node.table.table[node.id][i]:
                    node.table.table[node.id][i] = event.time
        
                
        log.close()
        
        
        #create calendar from it
        #using log file
        
        
        node.log = open("log.dat", "a+")

    def add(self, entry):
        if entry in self.calendar:
            return False
        else:
            self.calendar.append(entry)
            return True

    def delete(self, entry):
        if entry in self.calendar:
            self.calendar.remove(entry)
            return True
        else:
            return False

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)

    @staticmethod
    def load(js):
        a = EntrySet()
        a.__dict__ = js
        return a