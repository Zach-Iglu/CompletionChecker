
###################
## SVN File Object
###################
import os.path
import platform

import variables


# Special print function to print statuses
def dPrint(message, status="Stat", Logging=True):
    # Print File to Console
    print(status + " | " + message)

    # Log File
    if Logging:
        open("runLog.log", 'a').writelines(str(status) + " | " + message)

class uFile:
    """
    Ingests any filepath and converts it between os's
    Also some nice creature comforts
    """
    def __init__(self, filePath):
        self.original = filePath
        self.basename = os.path.basename(self.original)
        self.extension = str(self.original).split(".")[0]
        if "\\" in self.original:
            self.linuxPath = str(self.original).replace("\\", "/")
            self.windowsPath = self.original
        else:
            self.linuxPath = self.original
            self.windowsPath = str(self.original).replace("/", "\\")


    """
    Intuitively gives you the file path structure that you need
    """
    def path(self):
        if platform.system() == "Windows":
            return self.windowsPath
        else:
            return self.linuxPath

class SVNFile:
    """
    Keeps track of local and remote file paths
    """
    def __init__(self, local_location):
        self.local = uFile(local_location)
        self.remote = uFile(self.local.original.replace(SVN_LOCAL_REPO.path(), SVN_REMOTE_REPO.path()))

    """
    returns local path
    """
    def lpath(self):
        return self.local.path()

    """
    returns remote path
    """
    def rpath(self):
        return self.remote.path()

    def checkSyntaxRemote(self):
        command_to_check = "ssh " + variables.REMOTE_USER + "@" + variables.REMOTE_HOSTNAME + " " + SVN_SYNTAX_CHECK + " " + self.remote.path()
        dPrint("Checking Syntax of " + self.remote.basename + " (" + self.remote.original + ")" )
        dPrint(command_to_check, status="WARN")


SVN_LOCAL_REPO=uFile("/home/zach/scripts/ait/")
# SVN_LOCAL_REPO=uFile("O:\TC_old\maxar\AIT_repo_01_31_23")
# SVN_LOCAL_REPO=uFile("C:\\Users\\zholsing\\IdeaProjects\\icl2stol\\reference\\")
SVN_REMOTE_REPO=uFile("/scripts/ait/")
SVN_UPDATE_LOCAL="svn update " + SVN_LOCAL_REPO.path()
SVN_SYNTAX_CHECK="iclcheck -v OH43"