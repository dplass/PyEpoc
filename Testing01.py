# -*- coding: utf-8 -*-

from PyEpoc import *

EmotivEngine = EpocHandler()
choice = str()
engineeventhandle = EmotivEngine.EE_EmoEngineEventCreate()
statehandle = EmotivEngine.EE_EmoStateCreate()
EmotivEngine.ES_Init(statehandle)
UserID = 0

# Menu
print "A - Connect to EmoComposer\nB - Connect to Headset\nQ - Quit"
while (not isinstance(choice, str)) or ((choice != "a") and (choice != "b") and (choice != "q")):
    choice = raw_input("[A,B,Q] : ").lower()
    if choice == "q":
        quit()

# Connect
if choice == "a":
    if EmotivEngine.EE_EngineRemoteConnect("127.0.0.1",1726) != ERRCODE['EDK_OK']:
        print "Could not connect!"
        quit()
    else: print "Connected to EmoComposer!"    
elif choice == "b":
    if EmotivEngine.EE_EngineConnect() != ERRCODE['EDK_OK']:
        print "Could not connect!"
        quit()
    else: print "Connected to Headset!"

print """Engine Event handle at: %s""" %(engineeventhandle)
print """Emo State handle at: %s""" % (statehandle)

# Start 
while True:
    state = EmotivEngine.EE_EngineGetNextEvent(engineeventhandle)
    
    if state == ERRCODE['EDK_OK']:
        event = EmotivEngine.EE_EmoEngineEventGetType(engineeventhandle)
        user = EmotivEngine.EE_EmoEngineEventGetUserId(engineeventhandle)[1]
        if (event == EVENT['EE_EmoStateUpdated']):
            EmotivEngine.EE_EmoEngineEventGetEmoState(engineeventhandle,statehandle)
            #status
            battery = EmotivEngine.ES_GetBatteryChargeLevel(statehandle)
            wireless = EmotivEngine.ES_GetWirelessSignalStatus(statehandle)
            timestamp = EmotivEngine.ES_GetTimeFromStart(statehandle)
            #emo
            meditation = EmotivEngine.ES_AffectivGetMeditationScore(statehandle)
            shortexcitement = EmotivEngine.ES_AffectivGetExcitementShortTermScore(statehandle)
            longexcitement = EmotivEngine.ES_AffectivGetExcitementLongTermScore(statehandle)
            frustration = EmotivEngine.ES_AffectivGetFrustrationScore(statehandle)
            #cognitiv
            currentaction = EmotivEngine.ES_CognitivGetCurrentAction(statehandle)
            currentactionpower = EmotivEngine.ES_CognitivGetCurrentActionPower(statehandle)
            print """--------------------------------------------------------------------------------"""
            print """Timestamp: %s\tUser: %s\tEvent: %s\tW.Signal: %s\tBattery: %s""" % (timestamp,user,hex(event),wireless,battery)
            print """S.Excite: %s\tL.Excite: %s\tMeditation: %s\tFrustr: %s""" % (shortexcitement,longexcitement,meditation,frustration)
            print """Curr.Action: %s\tAction Pwr: %s""" % (hex(currentaction),currentactionpower)
