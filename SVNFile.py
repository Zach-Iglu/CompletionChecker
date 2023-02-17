
###################
## SVN File Object
###################
import datetime
import os.path
import platform
import subprocess

import variables


# Special print function to print statuses
def dPrint(message, status="STAT", Logging=True, onlyLog=False):
    if not onlyLog:
        # Print File to Console
        print(status + " | " + message)

    # Log File
    if Logging:
        with open("runLog.log", "a") as myfile:
            myfile.write(str(status) + " | " + message + "\n")

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
        self.basename = os.path.basename(local_location)
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
        beginTime = datetime.datetime.now()

        command_to_check = "ssh -X " + variables.REMOTE_USER + "@" + variables.REMOTE_HOSTNAME + " " + SVN_SYNTAX_CHECK + " " + self.remote.path()
        # dPrint("Checking Syntax of " + self.remote.basename)
        # dPrint(command_to_check, status="WARN")
        # Send Command
        command = subprocess.check_output(command_to_check, shell=True, stderr=subprocess.STDOUT)

        # Get Response
        response = command.decode("utf-8").split("\n")
        self.raw_response = response

        response.pop(0)  # Just a check
        self.errors = []
        self.critical_errors = []

        for error in response:
            error = error.strip()
            if len(error) > 0 and "strange command" not in error.lower():
                ## Each error is listed as a line, we clean it up and add it
                self.errors.append(error.strip())

                if ("close brace not aligned" not in error.lower()) and ("brace" in error.lower() or "bracket" in error.lower()):
                    self.critical_errors.append(error.strip())

                if "unknown" not in error.lower() and (("command" in error.lower() and "can't find command to check in" not in error.lower()) or "tlm" in error.lower() or "telemetry" in error.lower()):
                    self.critical_errors.append(error.strip())


        endTime = datetime.datetime.now()
        elapsed = (endTime - beginTime).seconds
        time = " (" + str(elapsed) + " Sec)"
        self.elapsed = elapsed

        if len(self.critical_errors) == 0:
            dPrint(self.remote.basename + time + " **Passed** ", status="PASS")
        else:
            dPrint(self.remote.basename + time + " FAILED with " + str(len(self.critical_errors)) + " Critical Errors", status="FAIL")

        # Log to File
        self.logReport()

    def logReport(self):
        """
        Prints Logs for Final Summary Generation
        :return:
        """
        """
        Error CSV Structure
        <file> <time> <status> <critical (y/n)> <error> <filepath>
        
        PASS CSV Structure
        <file> <time> <status> <total errors> <filepath>
        
        Summary CSV Structure
        <file> <time> <status> <total errors> <critical errors> <filepath>
        
        """
        status = "FAIL"
        if len(self.critical_errors) == 0:
            status = "PASS"
        baseStruct = self.remote.basename + ", " + datetime.datetime.today().strftime("%a %b %y") + ", " + status + ", "
        if len(self.critical_errors) != 0:
            for err in self.errors:
                if len(err.strip()) > 0:
                    if err in self.critical_errors:
                        errorLogEntry = baseStruct + "Y, " + err.replace(",", " ") + ", " + self.remote.path()
                        variables.dCritical(errorLogEntry)
                    else:
                        errorLogEntry = baseStruct + "N, " + err.replace(",", " ") + ", " + self.remote.path()
                        variables.dError(errorLogEntry)
        else:
            passLogEntry = baseStruct + str(len(self.errors)) + ", " + self.remote.path()
            variables.dPass(passLogEntry)

        summaryEntry = baseStruct + str(len(self.errors)) + ", " + str(len(self.errors)) + ", " + str(len(self.critical_errors)) + ", " + self.remote.path()
        variables.dSummary(summaryEntry)



SVN_LOCAL_REPO=uFile("/home/zach/scripts/ait/")
# SVN_LOCAL_REPO=uFile("C:\\Users\\zholsing\\IdeaProjects\\icl2stol\\reference\\")
SVN_REMOTE_REPO=uFile("/scripts/")
SVN_UPDATE_LOCAL="svn update " + SVN_LOCAL_REPO.path()
SVN_SYNTAX_CHECK="iclcheck -v OH43"