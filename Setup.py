import os
##########

# Statuses
import SVNFile
import variables


# Special print function to print statuses
def dPrint(message: str, status=variables.Status.STATUS, Logging=True):
    # Print File to Console
    print(status.value + " | " + message)

    # Log File
    if Logging:
        open("runLog.log", 'a').writelines(str(status) + " | " + message)


# Update SVN On Remote System
def updateSVNremote(parallel=False, verbose=False):
    if verbose:
        dPrint("Updating Remote SVN")
        dPrint("Parallel: " + str(parallel))
        dPrint("Sending Command: " + variables.SVN_UPDATE_REMOTE, status=variables.Status.WARN)
    if not parallel:
        os.system(variables.SVN_UPDATE_REMOTE)
    else:
        os.popen(variables.SVN_UPDATE_REMOTE)

# Update SVN on Local System
def updateSVNlocal(parallel=False, verbose=False):
    if verbose:
        dPrint("Updating Local SVN")
        dPrint("Parallel: " + str(parallel))
        dPrint("Sending Command: " + SVNFile.SVN_UPDATE_LOCAL, status=variables.Status.WARN)
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

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = filesInDir(dir, ext)
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