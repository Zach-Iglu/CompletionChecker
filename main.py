import threading

import Setup

def checkChunk(arrayOfSVNFiles):
    dPrint("Starting Thread")
    for svnFile in arrayOfSVNFiles:
        svnFile.checkSyntaxRemote()

# Special print function to print statuses
def dPrint(message, status="Stat", Logging=True, onlyLog=False):
    if not onlyLog:
        # Print File to Console
        print(status + " | " + message)

    # Log File
    if Logging:
        with open("runLog.log", "a") as myfile:
            myfile.write(str(status) + " | " + message + "\n")

if __name__ == "__main__":
    #Setup.updateSVNlocal()
    #Setup.updateSVNremote()

    Setup.cleanFiles()

    dPrint("Starting Threads")
    x = threading.Thread(target=checkChunk, args=(Setup.getLocalICL2Files(),))
    x.start()
    dPrint("Done Main Function")
