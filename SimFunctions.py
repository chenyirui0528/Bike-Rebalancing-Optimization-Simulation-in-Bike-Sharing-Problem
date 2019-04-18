# -*- coding: utf-8 -*-
"""
Converted from VBASim Basic Classes
initially by Yujing Lin for Python 2.7
Update to Python 3 by Linda Pei & Barry L Nelson
Last update 8/15/2018

"""

import SimClasses

def SimFunctionsInit(calendar,queues,ctstats,dtstats,resources):
    # Function to initialize SimFunctions.Python
    # Typically called before the first replication and between replications
    SimClasses.Clock = 0.0
    #Emply event calendar
    while (calendar.N() > 0):
        EV = calendar.Remove()
        
    #Empty queues
    #On first call, append the CStats created by FIFOQueue
    for Q in queues:
        if Q.WIP not in ctstats:
            ctstats.append(Q.WIP)
        while Q.NumQueue() > 0:
            En = Q.Remove()

    #Reinitialize Resources
    #On first call, append the CStats created by FIFOQueue and Resource
    for Re in resources:
        Re.Busy = 0.0
        if Re.NumBusy not in ctstats:
            ctstats.append(Re.NumBusy)  
    
    #Clear statistics
    for CT in ctstats:
        CT.Clear()
        CT.Xlast = 0.0   # added bln 
        
    for DT in dtstats:
        DT.Clear()
    



def Schedule(calendar,EventType, EventTime):
    #Schedule future events of EventType to occur at time SimClasses.Clock + EventTime
    
    addedEvent = SimClasses.EventNotice()
    addedEvent.EventType = EventType
    addedEvent.EventTime = SimClasses.Clock + EventTime
    # print("SimClasses.Clock is %f" % SimClasses.Clock)
    # print(EventTime)
    calendar.Schedule(addedEvent)
    

    
def SchedulePlus(calendar,EventType, EventTime, TheObject):
    #Schedule future events of EventType to occur at time SimClasses.Clock + EventTime
    #and pass with the event notice TheObject
    
    addedEvent = SimClasses.EventNotice()
    addedEvent.EventType = EventType
    addedEvent.EventTime = SimClasses.Clock + EventTime
    addedEvent.WhichObject = TheObject
    calendar.Schedule(addedEvent)
    
    
def ClearStats(ctstats,dtstats):
    #Clear statistics in TheDTStats and TheCTStats
    
    for CT in ctstats:
        CT.Clear()
    for DT in dtstats:
        DT.Clear()