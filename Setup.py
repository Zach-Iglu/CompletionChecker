import os
##########

# Statuses
import platform

import SVNFile
import variables

# Purges files to prepare for a new scan
def cleanFiles():
    dPrint("Cleaning Files", status="WARN")
    # purge error log
    try:
        os.remove("errors.csv")
    except:
        pass
    # purge pass log
    try:
        os.remove("pass.csv")
    except:
        pass
    # purge summary log
    try:
        os.remove("summary.csv")
    except:
        pass

    # purge summary log
    try:
        os.remove("critical.csv")
    except:
        pass



# Special print function to print statuses
def dPrint(message, status="STAT", Logging=True, onlyLog=False):
    if not onlyLog:
        # Print File to Console
        print(status + " | " + message)

    # Log File
    if Logging:
        with open("runLog.log", "a") as myfile:
            myfile.write(str(status) + " | " + message + "\n")

# Update SVN On Remote System
def updateSVNremote(parallel=False, verbose=True):
    if verbose:
        dPrint("Updating Remote SVN")
        dPrint("Parallel: " + str(parallel))
        dPrint("Sending Command: " + variables.SVN_UPDATE_REMOTE, status="WARN")
    if not parallel:
        os.system(variables.SVN_UPDATE_REMOTE)
    else:
        os.popen(variables.SVN_UPDATE_REMOTE)

# Update SVN on Local System
def updateSVNlocal(parallel=False, verbose=True):
    if verbose:
        dPrint("Updating Local SVN")
        dPrint("Parallel: " + str(parallel))
        dPrint("Sending Command: " + SVNFile.SVN_UPDATE_LOCAL, status="WARN")
    if not parallel:
        os.system(SVNFile.SVN_UPDATE_LOCAL)
    else:
        os.popen(SVNFile.SVN_UPDATE_LOCAL)

"""
Quickly Gets All Files Of Specifc Extension With Full Filepath

From: https://stackoverflow.com/questions/18394147/how-to-do-a-recursive-sub-folder-search-and-return-files-in-a-list
"""
def filesInDir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.listdir(dir):
        f = dir + f
        if os.path.isdir(f):
            subfolders.append(f)
        if os.path.isfile(f):
            # extension = f.split(".")[-1]
            # if extension == "icl2":
            if "." + f.split(".")[-1] in ext:
                files.append(f)

    for dir in subfolders:
        if platform.system() == "Windows":
            sf, f = filesInDir(dir + "\\", ext)
        else:
            sf, f = filesInDir(dir + "/", ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files

# Get List of ICL2 Scripts From Local System
def getLocalICL2Files():
    dPrint("Getting All .icl2 Files To Check")
    ## List all files recursively inside directory specified
    subfolders, files = filesInDir(SVNFile.SVN_LOCAL_REPO.path(), [".icl2"])
    dPrint("Need to Check " + str(len(files)) + " Files")

    SVN_Scripts = []

    ## instantiate each one as an SVN file
    for file in files:
        temp = SVNFile.SVNFile(file)
        SVN_Scripts.append(temp)

    ## return svnfile type list
    return SVN_Scripts