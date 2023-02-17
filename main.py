import SVNFile
import Setup

if __name__ == "__main__":
    svnFiles = Setup.getLocalICL2Files()
    for svnFile in svnFiles:
        svnFile.checkSyntaxRemote()