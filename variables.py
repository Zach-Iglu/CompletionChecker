# Locations

# Remote Computer
import time

REMOTE_HOSTNAME="osam-das"
REMOTE_USER="das" # Assume RSA-Pair

# Commands
SVN_UPDATE_REMOTE_COMMAND="svnops update"
SVN_UPDATE_REMOTE="ssh " + REMOTE_USER + "@" + REMOTE_HOSTNAME + " " + SVN_UPDATE_REMOTE_COMMAND

wErr = False
wCrit = False
wPass = False
wSum = False

# Logs Error to File
def dError(message):
    global wErr
    while wErr == True:
        time.sleep(0.1)
    wErr = True
    with open("errors.csv", "a") as myfile:
        myfile.write(message + "\n")
    wErr = False

# Logs Error to File
def dCritical(message):
    global wCrit
    while wCrit == True:
        time.sleep(0.1)
    wCrit = True
    with open("critical.csv", "a") as myfile:
        myfile.write(message + "\n")
    wCrit = False

# Logs Passes to File
def dPass(message):
    global wPass
    while wPass == True:
        time.sleep(0.1)
    wPass = True
    with open("pass.csv", "a") as myfile:
        myfile.write(message + "\n")
    wPass = False

# Logs Passes to File
def dSummary(message):
    global wSum
    while wSum == True:
        time.sleep(0.1)
    wSum = True
    with open("summary.csv", "a") as myfile:
        myfile.write(message + "\n")
    wSum = False