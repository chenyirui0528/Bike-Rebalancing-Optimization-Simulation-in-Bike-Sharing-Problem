# -*- coding: utf-8 -*-
"""
Converted from VBASim Basic Classes
initially by Yujing Lin for Python 2.7
Update to Python 3 by Linda Pei & Barry L Nelson
Last update 8/15/2018
"""
import math

Clock = 0

class Activity():
    # Object to model and activity-destination node pair
    def __init__(self):
        self.WhichActivity = 0
        self.WhichNode = 0
    
class CTStat():
    # Generic continuous-time statistics object
    # Note that CTStat should be called AFTER the value of the variable changes

    def __init__(self):
        # Excecuted when the CTStat object is created to initialize variables
        self.Area = 0.0
        self.Tlast = 0.0
        self.TClear = 0.0
        self.Xlast = 0.0
        
    def Record(self,X):
        # Update the CTStat from the last time change and keep track of previous value
        self.Area = self.Area + self.Xlast * (Clock - self.Tlast)
        self.Tlast = Clock
        self.Xlast = X

    def Mean(self):
        # Return the sample mean up through the current time but do not update
        mean = 0.0
        if (Clock - self.TClear) > 0.0:
           mean = (self.Area + self.Xlast * (Clock - self.Tlast)) / (Clock - self.TClear)
        return mean
    
    def Clear(self):
        # Clear statistics
        self.Area = 0.0
        self.Tlast = Clock
        self.TClear = Clock


class DTStat():
    # Generic discrete-time statistics object

    def __init__(self):
        # Excecutes when the DTStat object is created to initialize variables
        self.Sum = 0.0
        self.SumSquared = 0.0
        self.NumberOfObservations = 0.0
    
    def Record(self,X):
        # Update the DTStat
        self.Sum = self.Sum + X
        self.SumSquared = self.SumSquared + X * X
        self.NumberOfObservations = self.NumberOfObservations + 1
        
    def Mean(self):
        # Return the sample mean
        mean = 0.0
        if self.NumberOfObservations > 0.0:
            mean = self.Sum / self.NumberOfObservations
        return mean

    def StdDev(self):
        # Return the sample standard deviation
        stddev = 0.0
        if self.NumberOfObservations > 1.0:
            stddev = math.sqrt((self.SumSquared - self.Sum**2 / self.NumberOfObservations) / (self.NumberOfObservations - 1))
        return stddev
            
    def N(self):
        # Return the number of observations collected
        return self.NumberOfObservations
    
    def Clear(self):
        # Clear statistics
        self.Sum = 0.0
        self.SumSquared = 0.0
        self.NumberOfObservations = 0.0
        

class Entity():
    # This is the generic Entity that has a single attribute CreateTime
    def __init__(self):
        # Executes with the Entity object is created to initialize variables
        # Add additional problem-specific attributes here
        self.CreateTime = Clock
        self.ClassNum = 0
        

        
class EventNotice():
    # This is the generic EventNotice object with EventTime, EventType and 
    # WhichObject attributes
    # Add additional problem-specific attributes here
    def __init__(self):
        self.EventTime = 0.0
        self.EventType = ""
        self.WhichObject = ()
        
        
class EventCalendar():
    # This class creates an EventCalendar object which is a list of
    # EventNotices ordered by time. Based on an object created by Steve Roberts.

    def __init__(self):
        self.ThisCalendar = []   
    def Schedule(self,addedEvent):
        # Add EventNotice in EventTime order
        if len(self.ThisCalendar) == 0:  #no events in calendar
            self.ThisCalendar.append(addedEvent)
        elif self.ThisCalendar[-1].EventTime <= addedEvent.EventTime:
            self.ThisCalendar.append(addedEvent)
        else:
            for rep in range(0,len(self.ThisCalendar),1):
                if self.ThisCalendar[rep].EventTime > addedEvent.EventTime:
                    break
            self.ThisCalendar.insert(rep,addedEvent)
    
    def Remove(self):
        # Remove next event and return the EventNotice object
        if len(self.ThisCalendar) > 0:
            return self.ThisCalendar.pop(0)
        
    def N(self):
        # Return current number of events on the event calendar
        return len(self.ThisCalendar)
    
class FIFOQueue():
    # This is a generic FIFO Queue object that also keeps track
    # of statistics on the number in the queue (WIP)

    def __init__(self):
        # Executes when the FIFOQueue object is created to add queue statistics
        # to TheCTStats list
        self.WIP = CTStat()
        self.ThisQueue = []
        
    def NumQueue(self):
        # Return current number in the queue
        return len(self.ThisQueue)
        
    def Add(self,X):
        # Add an entity to the end of the queue
        self.ThisQueue.append(X)
        numqueue = self.NumQueue()
        self.WIP.Record(float(numqueue))    
    
    def Remove(self):
        # Remove the first entity from the queue and return the object
        # after updating the queue statistics
        if len(self.ThisQueue) > 0:
            remove = self.ThisQueue.pop(0)
            self.WIP.Record(float(self.NumQueue()))
            return remove
        
    def Mean(self):
        # Return the average number in queue up to the current time
        return self.WIP.Mean()
        
class Resource():
    # This is a generic Resource object that also keeps track of statistics
    # on number of busy resources

    def __init__(self):
        # Executes when the resource object is created to initialize variables
        # and add number of busy Resources statistic to TheCTStats list
        self.Busy = 0
        self.NumberOfUnits = 0
        self.NumBusy = CTStat()
        
    def Seize(self, Units):
        # Seize Units of resource then update statistics
        # Returns False and does not seize if not enouge resources available;
        # otherwise returns True
        diff = self.NumberOfUnits - Units - self.Busy
        if diff >= 0:
            # If diff is nonnegative, then there are enough resources to seize
            self.Busy = self.Busy + Units
            self.NumBusy.Record(float(self.Busy))
            seize = True
        else:
            seize = False
        return seize
        
    def Free(self, Units):
        # Frees Units of resource then update statistics
        # Returns False and does not free if attempting to free more resources than available;
        # otherwise returns True
        diff = self.Busy - Units
        # If diff is negative, then trying to free too many resources
        if diff < 0:
            free = False
        else:
            self.Busy = self.Busy - Units
            self.NumBusy.Record(float(self.Busy))
            free = True
        return free
    
    def Mean(self):
        # Returtime-average number of busy resources up to current time
        return self.NumBusy.Mean()
        
    def SetUnits(self, Units):
        # Set the capacity of the resource (number of identical units)
        self.NumberOfUnits = Units
        
