# beaconframer --os mac
# beaconframer --help
# windows and mac currently not supported only linux
# storm example:  python beaconFramer.py -v -i wlan0 --storm

import sys
import os
import argparse
import datetime
import time
from threading import Thread
import subprocess
import shlex
import time
import threading
import platform
import subprocess
from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump,RandMAC

locky = threading.Lock()

os.system("clear")

version = "1.0.0"
operationSystem = None
verbose = False
interfaceName = None
monitorInterface = None


def displayWelcomeText():
    print "############################################################################"
    print """
  ____                                 _____                              
 | __ )  ___  __ _  ___ ___  _ __     |  ___| __ __ _ _ __ ___   ___ _ __ 
 |  _ \ / _ \/ _` |/ __/ _ \| '_ \    | |_ | '__/ _` | '_ ` _ \ / _ \ '__|
 | |_) |  __/ (_| | (_| (_) | | | |   |  _|| | | (_| | | | | | |  __/ |   
 |____/ \___|\__,_|\___\___/|_| |_|   |_|  |_|  \__,_|_| |_| |_|\___|_|   
                                                                        
                                                                        """
    print "############################################################################"

#########################################################################
def log(string):
    global verbose
    if(verbose):
        st = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print "[", st, "] ", string

def logAnywhere(string):
    st = datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print "[", st, "] ", string

def cleanUpInterface():
    global interfaceName

    os.system("airmon-ng stop {}".format(interfaceName + "mon"))
    os.system("service network-manager start")

#########################################################################

def cleanUp():
    cleanUpInterface()


def detectOperationSystem():
    returnVal = None
    systemName = platform.system().upper()
    if systemName == 'Darwin'.upper():
        log("Detected Operation System: Mac Os is running")
        returnVal = 'mac'
    elif systemName == 'LINUX':
        log("Detected Operation System: Linux is running")
        returnVal = 'lin'
    elif systemName == '':
        log("Detected Operation System: Windows is running")
        returnVal = 'win'
    else:
	log("Operation system not detected! Found: {}".format(systemName))
	print "Exiting Program"
	sys.exit()

    return returnVal


def setMonitorMode():
    global operationSystem

    if operationSystem == 'mac':
        setMonitorModeMac()
    elif operationSystem == 'lin':
        setMonitorModeLin()

def setMonitorModeLin():
    global interfaceName
    global monitorInterface
   
    
    log("Monitoring mode for linux!")
    os.system("service network-manager stop")
    

    interfaceAirmon = os.system("airmon-ng start {}".format(interfaceName))

    if interfaceAirmon != 0:
	logAnywhere("Error while setting Interface {} into monitor mode. Cause: Unsupported wireless card or wrong interface name".format(interfaceName))
	sys.exit()

    log("Interface {} set in monitor mode".format(interfaceName))
    monitorInterface = interfaceName + "mon"

def setMonitorModeMac():

    if os.path.exists('/usr/local/bin/airport') == False:
        log("Setting systemlink for airport commands at '/usr/local/bin/airport'")
        print "Please enter Password to take further actions!"
        os.system("sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport")


def stormWithBeaconFrames():
    global interfaceName
    global monitorInterface
    log("Starting with storming on interface [{}]".format(interfaceName))
    
    netSSID = 'testSSID'       #Network name here
    iface = 'wlan0mon'         #Interface name here

    dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=str(RandMAC()), addr3=str(RandMAC()))
    
    beacon = Dot11Beacon(cap='ESS+privacy')
    essid = Dot11Elt(ID='SSID',info=netSSID, len=len(netSSID))
    rsn = Dot11Elt(ID='RSNinfo', info=(
'\x01\x00'                 #RSN Version 1
'\x00\x0f\xac\x02'         #Group Cipher Suite : 00-0f-ac TKIP
'\x02\x00'                 #2 Pairwise Cipher Suites (next two lines)
'\x00\x0f\xac\x04'         #AES Cipher
'\x00\x0f\xac\x02'         #TKIP Cipher
'\x01\x00'                 #1 Authentication Key Managment Suite (line below)
'\x00\x0f\xac\x02'         #Pre-Shared Key
'\x00\x00'))               #RSN Capabilities (no extra capabilities)

    frame = RadioTap()/dot11/beacon/essid/rsn

    frame.show()
    print("\nHexdump of frame:")
    hexdump(frame)
    raw_input("\nPress enter to start\n")

    sendp(frame, iface=iface, inter=0.100, loop=1)


    

def main():
    global verbose
    global operationSystem
    global interfaceName

    displayWelcomeText()

    print "\n"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--interface', help='Which interface card you want to use to analyse the area around you.', required=True)
    parser.add_argument(
        '-s', '--storm', dest='storm', action='store_true', help='Storms the area around you with AP from the list')

    parser.add_argument(
        '-os', help="Defines which operation system you are using. Format [mac/win/lin]")
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='Set if you would like to recive log informations')
    parser.add_argument('--cleanUp', dest='cleanUp', action='store_true',
                        help='Cleans up every change made by the script')

    args, leftovers = parser.parse_known_args()

    verbose = args.verbose

    interfaceName = args.interface

    # Clean up
    if args.cleanUp:
	log("Cleaning up all changes made by the script")
	#cleanUp()
	log("Finished with cleaning! Have a nice day :)")
	sys.exit()

    # Analyzing the os flag
    if args.os == None:
        log("Operation System is not set, we have to autodetec it")
        operationSystem = detectOperationSystem()
    else:
        log("Operation System is set, no autodetect needed")
        operationSystem = args.os

    
    # setting card into monitor mode
    log("Starting to set interface in monitor mode")
    #setMonitorMode()

    if args.storm:
	stormWithBeaconFrames()



if __name__ == "__main__":
    main()
    print "\n"
