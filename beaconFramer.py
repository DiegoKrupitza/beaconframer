# beaconframer --os mac
# beaconframer --help
# windows and mac currently not supported

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

locky = threading.Lock()

os.system("clear")

version = "1.0.0"
operationSystem = None
verbose = False
interfaceName = None


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

    log("Monitoring mode for linux!")
    try:
    	subprocess.call(["sudo ifconfig {} down".format(interfaceName)])
    	subprocess.call(["sudo iwconfig {} mode monitor".format(interfaceName)])
    except OSError:
	logAnywhere("Error while setting Interface {} into monitor mode. Cause: Unsupported wireless card or wrong interface name".format(interfaceName))
	sys.exit()
    log("Interface {} set in monitor mode".format(interfaceName))

def setMonitorModeMac():

    if os.path.exists('/usr/local/bin/airport') == False:
        log("Setting systemlink for airport commands at '/usr/local/bin/airport'")
        print "Please enter Password to take further actions!"
        os.system("sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/local/bin/airport")


def Change_Freq_channel(channel_c):
    # TODO change
    print('Channel:', str(channel_c))
    command = 'iwconfig wlan1mon channel '+str(channel_c)
    command = shlex.split(command)
    # To prevent shell injection attacks !
    subprocess.Popen(command, shell=False)


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
        '-s', '--storm', help='Storms the area around you with AP from the list')

    parser.add_argument(
        '-os', help="Defines which operation system you are using. Format [mac/win/lin]")
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='Set if you would like to recive log informations')

    args, leftovers = parser.parse_known_args()

    verbose = args.verbose

    if args.os == None:
        log("Operation System is not set, we have to autodetec it")
        operationSystem = detectOperationSystem()
    else:
        log("Operation System is set, no autodetect needed")
        operationSystem = args.os

    interfaceName = args.interface

    log("Starting to set interface in monitor mode")
    setMonitorMode()


if __name__ == "__main__":
    main()
    print "\n"
