import SVNFile
import Setup

if __name__ == "__main__":
    Setup.updateSVNlocal()
    Setup.updateSVNremote()

    Setup.cleanFiles()

    svnFiles = Setup.getLocalICL2Files()


    for svnFile in svnFiles:
        svnFile.checkSyntaxRemote()