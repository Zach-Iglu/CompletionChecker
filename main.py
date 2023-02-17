import os
import threading
import time
from itertools import islice
from math import ceil

import Setup
from variables import closeFiles


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

    SINGLE_THREAD_TIME_SEC = 17

    total_time_hours = ((float(SINGLE_THREAD_TIME_SEC) * float(realistic_chunksize)) / 60)
    dPrint("Starting " + str(ThreadCount) + " Threads with ~" + str(realistic_chunksize) + " Scripts Per Thread", status="WARN")
    dPrint("Est. " + str(total_time_hours) + " Minutes to Complete")
    time.sleep(5)
    index = 0
    threads = []

    for sample in make_chunks(masterFileList, CHUNKSIZE):
        x = threading.Thread(target=checkChunk, args=(sample, index))
        x.start()
        threads.append(x)
        index += 1

    for thread in threads:
        thread.join()

    closeFiles()
    dPrint("All Threads Done, Generating Summary")
