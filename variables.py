# Locations

# Remote Computer
REMOTE_HOSTNAME="osam-das"
REMOTE_USER="das" # Assume RSA-Pair

# Commands
SVN_UPDATE_REMOTE_COMMAND="svnops update"
SVN_UPDATE_REMOTE="ssh " + REMOTE_USER + "@" + REMOTE_HOSTNAME + " " + SVN_UPDATE_REMOTE_COMMAND

# Logs Error to File
def dError(message):
        with open("errors.csv", "a") as myfile:
            myfile.write(message + "\n")

# Logs Error to File
def dCritical(message):
    with open("critical.csv", "a") as myfile:
        myfile.write(message + "\n")

# Logs Passes to File
def dPass(message):
    with open("pass.csv", "a") as myfile:
        myfile.write(message + "\n")

# Logs Passes to File
def dSummary(message):
    with open("summary.csv", "a") as myfile:
        myfile.write(message + "\n")