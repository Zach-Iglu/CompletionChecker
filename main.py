import os
import threading
import time
from itertools import islice
from math import ceil

import Setup

def checkChunk(arrayOfSVNFiles, threadCount):
    dPrint("Starting Thread " + str(threadCount))
    for svnFile in arrayOfSVNFiles:
        try:
            svnFile.checkSyntaxRemote()
        except Exception as e:
            dPrint("Script " + os.path.basename(svnFile.rpath()) + " Broke :( ", status="FAIL")

# Special print function to print statuses
def dPrint(message, status="STAT", Logging=True, onlyLog=False):
    if not onlyLog:
        # Print File to Console
        print(status + " | " + message)

    # Log File
    if Logging:
        with open("runLog.log", "a") as myfile:
            myfile.write(str(status) + " | " + message + "\n")

def make_chunks(data, SIZE):
    it = iter(data)
    # use `xragne` if you are in python 2.7:
    for i in range(0, len(data), SIZE):
        yield [k for k in islice(it, SIZE)]

if __name__ == "__main__":
    #Setup.updateSVNlocal()
    #Setup.updateSVNremote()

    Setup.cleanFiles()

    masterFileList = Setup.getLocalICL2Files()

    # Specify how many per thread and it will calculate how many threads to make
    CHUNKSIZE = 100
    ThreadCount = int(ceil(float(len(masterFileList)) / float(CHUNKSIZE)))


    size = 0
    for sample in make_chunks(masterFileList, CHUNKSIZE):
        size = len(sample)
        break

    realistic_chunksize = size
    dPrint("Starting " + str(ThreadCount) + " Threads with ~" + str(realistic_chunksize) + " Scripts Per Thread", status="WARN")
    time.sleep(2)
    index = 0
    threads = []

    for sample in make_chunks(masterFileList, CHUNKSIZE):
        x = threading.Thread(target=checkChunk, args=(sample, index))
        x.start()
        threads.append(x)
        index += 1

    for thread in threads:
        thread.join()
    # dPrint("All Threads Done, Generating Summary")
