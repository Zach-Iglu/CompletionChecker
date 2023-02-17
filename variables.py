# Locations

# Remote Computer
REMOTE_HOSTNAME="osam-das"
REMOTE_USER="das" # Assume RSA-Pair

# Commands
SVN_UPDATE_REMOTE_COMMAND="svnops update"
SVN_UPDATE_REMOTE="ssh " + REMOTE_USER + "@" + REMOTE_HOSTNAME + " " + SVN_UPDATE_REMOTE_COMMAND

derr = open("errors.csv", "a")
dcrit = open("critical.csv", "a")
dpass = open("pass.csv", "a")
dsum = open("summary.csv", "a")

def closeFiles():
    derr.close()
    dcrit.close()
    dpass.close()
    dsum.close()

# Logs Error to File
def dError(message):
    global derr
    derr.write(message + "\n")

# Logs Error to File
def dCritical(message):
    global dcrit
    dcrit.write(message + "\n")

# Logs Passes to File
def dPass(message):
    global dpass
    dpass.write(message + "\n")

# Logs Passes to File
def dSummary(message):
    global dsum
    dsum.write(message + "\n")