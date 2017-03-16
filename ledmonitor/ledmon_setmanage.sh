#!/bin/bash
#
#
# ledmon_setmanage
#   -c clear state and remove statefile
#   -s set state. Options are: managed, unmanaged
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
    echo "      ${REV}-s${NORM}  Sets the Manage state. Valid choices are: ${BOLD}managed${NORM} and ${BOLD}unmanaged${NORM}."
    echo "      ${REV}-c${NORM}  Clears the manage state by removing the state file."
    echo "      ${REV}-h${NORM}  Displays this help message."
    echo "  Running the script with no arguments, returns the Manage state if present."
    exit 1
}

# Check the number of arguments. If none are passed return the contents of the manage.state file.
NUMARGS=$#
if [ $NUMARGS -eq 0 ]; then
    echo "Manage state currently set to:" `cat <./manage.state`
fi

while getopts :s:ch FLAG; do
    case $FLAG in
        c)  # clear state
            OPT_C=$OPTARG
            rm ./manage.state
            exit 0
            ;;
        s)  # set state
            OPT_S=$OPTARG
            if [ $OPT_S = "managed" ]
                then
                    echo "managed" > ./manage.state
                    exit 0
            fi
            if [ $OPT_S = "unmanaged" ]
                then
                    echo "unmanaged" > ./manage.state
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
