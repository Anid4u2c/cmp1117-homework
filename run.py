from calendar import getDate, getSchedule, scheduleCheck
from config import configGet
from fileActions import fileCreate, filesList, fileNameGet, fileRename, OPTIONS_FILE
from helpers import printOptions

OPTIONS_NAME = {1: "Allow the application to name the file for you.", 2: "Specify a name for your file.", 3: "GO BACK"}
OPTIONS = {1: "Create a file for an assignment", 2: "List all assignment files", 3: "Rename a assignment file",
           4: "QUIT"}

def actionGet(option):
    if option is None:
        option = ""
    if option in OPTIONS.keys():
        print("\t\tOkay, let's " + OPTIONS[option].lower() + "...")
        if option == 1:
            fileType = OPTIONS_FILE[printOptions(OPTIONS_FILE)]
            if fileType != "GO BACK":
                fileNameOption = printOptions(OPTIONS_NAME)
                if fileNameOption == 2:
                    fileName = input("\r\n\tWhat would you like to name your {} file?  ".format(fileType))
                else:
                    fileName = fileNameGet(fileType)
                fileCreate(fileName, fileType)
            else:
                actionGet(printOptions(OPTIONS))
        elif option == 2:
            for folder in ("homework", "labs"):
                filesList(folder)
        elif option == 3:
            fileRename()
        else:
            quit()

def assignmentsFilter(dateString, config):
    today = dateString
    scheduleData = getSchedule()
    dates = scheduleData["list"]
    courseData = scheduleData["dictionary"]
    if scheduleCheck(today, dates):
        assignment = courseData[today]
        print("\r\n\tThere's an assignment today:  ")
        print("\t\tFor {}, in week {}".format(today, assignment["Week"]))
        for key in sorted(assignment.keys()):
            if key not in ["Date", "Week", "Class", "Day"]:
                print("\t\t", key + ":  ", assignment[key])
        response = input("\r\n\tWould you like to create a file for this assignment ('N' = 'no', 'Y' = 'yes'):  ")
        if response.upper() in ["Y", "YES"] and len(response) > 0:
            print("\t\tOkay, we'll create a file named:  ch{}.".format(assignment["Chapter"].lower()))
    else:
        print("\r\n\tThere's no assignment today...")
    actionGet(printOptions(OPTIONS))

def main():
    config = configGet()
    # webbrowser.open('file://' + os.path.realpath(FILENAME))
    today = getDate()
    # today = "2019-11-21"
    print("\r\n\tGreat {}!  Today's date is {}...".format(config["firstName"], today))
    assignmentsFilter(today, config)


main()
