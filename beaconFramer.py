# beaconframer --os mac
# beaconframer --help

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
locky = threading.Lock()

os.system("clear")

version = "1.0.0"
operationSystem = None
verbose = False


def showHelpInformation():
    print "\n"
    print "You are using the version", version
    print """
This is the help text for Beacon Framer
    --os [mac/win/lin]      which operating system are you using 
    
    """


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


def detectOperationSystem():
    returnVal = None
    systemName = platform.system().upper()
    if systemName == 'Darwin'.upper():
        log("Detected Operation System: Mac Os is running")
        returnVal = 'mac'
    elif systemName == '':
        log("Detected Operation System: Linux is running")
        returnVal = 'lin'
    elif systemName == '':
        log("Detected Operation System: Windows is running")
        returnVal = 'win'

    return returnVal


def setMonitorMode():
    global operationSystem

    if operationSystem == 'mac':
        setMonitorModeMac()
    elif operationSystem == 'lin':
        setMonitorModeLin()

def setMonitorModeLin():
    log("Monitoring mode for linux!")

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

    log("Starting to set interface in monitor mode")
    setMonitorMode()


if __name__ == "__main__":
    main()
    print "\n"
