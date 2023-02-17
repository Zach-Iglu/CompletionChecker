import datetime
import os
import threading
import time
from itertools import islice
from math import ceil
from random import randint

import Setup


def checkChunk(arrayOfSVNFiles, threadCount):
    time.sleep(randint(1, 30))
    dPrint("Starting Thread " + str(threadCount))
    retryFiles = []
    MAXRETRYCOUNT = 10
    for svnFile in arrayOfSVNFiles:
        try:
            svnFile.checkSyntaxRemote()
        except Exception as er:
            dPrint("Script " + os.path.basename(svnFile.rpath()) + " Broke on Thread " + str(threadCount) + " :( ", status="FAIL")
            with open("error_" + str(threadCount) + ".log", 'a') as f:
                f.write(str(er) + "\n")
            retryFiles.append(svnFile)
    retryCount = 1
    while len(retryFiles) != 0 and retryCount < MAXRETRYCOUNT:
        dPrint("(" + str(retryCount) + "/" + str(MAXRETRYCOUNT) + ") Retrying Thread " + str(threadCount) + " With " + str(len(retryFiles)) + " Files")
        errors = []
        for svnFile in retryFiles:
            try:
                svnFile.checkSyntaxRemote()
            except Exception as er:
                dPrint("Script " + os.path.basename(svnFile.rpath()) + " Broke on Thread " + str(threadCount) + " :( ", status="FAIL")
                with open("error_" + str(threadCount) + ".log", 'a') as f:
                    f.write(str(er) + "\n")
                errors.append(svnFile)
        retryFiles = errors
        retryCount += 1

    # Print that we are giving up on specific scripts
    for script in retryFiles:
        dPrint("Giving up on " + os.path.basename(script.rpath()) + " :( ", status="CRIT")




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
    CHUNKSIZE = 10
    ThreadCount = int(ceil(float(len(masterFileList)) / float(CHUNKSIZE)))


    size = 0
    for sample in make_chunks(masterFileList, CHUNKSIZE):
        size = len(sample)
        break

    realistic_chunksize = size

    SINGLE_THREAD_TIME_SEC = 17

    total_time_hours = ((float(SINGLE_THREAD_TIME_SEC) * float(realistic_chunksize)) / 60)
    dPrint("Starting " + str(ThreadCount) + " Threads with ~" + str(realistic_chunksize) + " Scripts Per Thread", status="WARN")
    dPrint("Est. " + str(total_time_hours) + " Minutes to Complete")
    time.sleep(5)
    index = 0
    threads = []

    beginTime = datetime.datetime.now()
    for sample in make_chunks(masterFileList, CHUNKSIZE):
        x = threading.Thread(target=checkChunk, args=(sample, index))
        x.start()
        threads.append(x)
        index += 1

    for thread in threads:
        thread.join()

    endTime = datetime.datetime.now()
    elapsed = (endTime - beginTime).seconds
    dPrint("(" + str(elapsed) + " Sec) All Threads Done, Generating Summary")
