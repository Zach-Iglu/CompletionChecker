# Locations

# Remote Computer

REMOTE_HOSTNAME="osam-das"
REMOTE_USER="das" # Assume RSA-Pair

# Commands
SVN_UPDATE_REMOTE_COMMAND="svnops update"
SVN_UPDATE_REMOTE="ssh " + REMOTE_USER + "@" + REMOTE_HOSTNAME + " " + SVN_UPDATE_REMOTE_COMMAND