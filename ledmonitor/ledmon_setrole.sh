#!/bin/bash
#
#
# ledmon_setrole
#   -c clear state and remove statefile
#   -s set state. Options are: gateway, development, test, production
#

#Set Script Name variable
SCRIPT=`basename ${BASH_SOURCE[0]}`

#Initialize variables to default values.
OPT_C=C
OPT_S=S

#Set fonts for Help.
NORM=`tput sgr0`
BOLD=`tput bold`
REV=`tput smso`

#Help function
function HELP {
    echo -e "${REV}Usage:${NORM} ${BOLD}$SCRIPT ${NORM}"
    echo "  The following options are recognized."
    echo "      ${REV}-s${NORM}  Sets the Role state. Valid choices are: ${BOLD}web${NORM}, ${BOLD}application${NORM}, ${BOLD}server${NORM} and ${BOLD}database${NORM}."
    echo "      ${REV}-c${NORM}  Clears the Role state by removing the state file."
    echo "      ${REV}-h${NORM}  Displays this help message."
    echo "  Running the script with no arguments, returns the Role state if present."
    exit 1
}

# Check the number of arguments. If none are passed return the contents of the role.state file.
NUMARGS=$#
if [ $NUMARGS -eq 0 ]; then
    echo "Role state currently set to:" `cat <./role.state`
fi

while getopts :s:ch FLAG; do
    case $FLAG in
        c)  # clear state
            OPT_C=$OPTARG
            rm ./role.state
            exit 0
            ;;
        s)  # set state
            OPT_S=$OPTARG
            if [ $OPT_S = "web" ]
                then
                    echo "web" > ./role.state
                    exit 0
            fi
            if [ $OPT_S = "application" ]
                then
                    echo "application" > ./role.state
                    exit 0
            fi  
            if [ $OPT_S = "server" ]
                then
                    echo "server" > ./role.state
                    exit 0
            fi  
            if [ $OPT_S = "database" ]
                then
                    echo "database" > ./role.state
                    exit 0
            fi  
            echo "Invalid state: ${BOLD}$OPT_S${NORM}. No changes made." 1>&2
            echo "Use ${BOLD}$SCRIPT -h${NORM} for help." 1>&2
            exit 1
            ;;
        h)  # show help
            HELP
            ;;
        :)
            echo "Invalid option: ${BOLD}$OPTARG${NORM} requires an argument. No changes made." 1>&2
            echo "Use ${BOLD}$SCRIPT -h${NORM} for help." 1>&2
            exit 1
        ;;
        \?) # unrecognized option
            echo "Option -${BOLD}$OPTARG${NORM} not allowed. No changes made." 1>&2
            echo "Use ${BOLD}$SCRIPT -h${NORM} for help." 1>&2
            exit 1
            ;;
    esac
done
echo "Missing argument. No changes made." 1>&2
echo "Use ${BOLD}$SCRIPT -h${NORM} for help." 1>&2
exit 1

shift $((OPTIND-1))  #This tells getopts to move on to the next argument.

