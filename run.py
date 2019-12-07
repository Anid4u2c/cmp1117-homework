from calendar import getDate, getSchedule, scheduleCheck
from config import configGet
from fileActions import fileCreate, fileNameGet, filesList, OPTIONS_FILE, SUBFOLDERS
from helpers import addOption, printOptions

OPTIONS_NAME = {1: "Allow the application to name the file for you.", 2: "Specify a name for your file."}
OPTIONS = {1: "Create a file for an assignment", 2: "List all assignment files", 3: "Rename a assignment file"}

def actionGet(options):
    option = printOptions(options)
    while option != len(OPTIONS.keys()):
        print("\n\t\tOkay, let's " + OPTIONS[option].lower() + "...")
        if option == 1:
            fileType = printOptions(addOption(OPTIONS_FILE, "GO BACK"))
            while fileType != len(OPTIONS_FILE.keys()):
                fileNameOption = printOptions(addOption(OPTIONS_NAME, "GO BACK"))
                while fileNameOption != len(OPTIONS_NAME.keys()):
                    if fileNameOption == 2:
                        fileType = OPTIONS_FILE[fileType]
                        fileName = input("\n\tWhat would you like to name your {} file?  ".format(fileType))
                    else:
                        fileName = fileNameGet(fileType)
                    fileCreate(fileName, fileType)
                fileType = len(OPTIONS_FILE)
            actionGet(options)
        elif option == 2:
            filesList(SUBFOLDERS)
            print("\n\t\tFinished " + OPTIONS[option].lower() + ".")
            actionGet(printOptions(OPTIONS))
        elif option == 3:
            filesByFolder = filesList(SUBFOLDERS)
            for folder in filesByFolder.keys():
                printOptions(buildChoicesForFiles(filesByFolder))
            '''
            for folder, files in filesByFolder.items():
                print("\n\t\t You have {} files in the directory '{}'".format(folder, len(files)))
                if len(files) > 0:
                    for file in files:
                        listOfFiles.append(path.join(folder, file))
                else:
                    print("\n\t\t You have 0 files in all directories, try creating some files first.")
            '''
        #print("\n\t\tOkay, let's " + OPTIONS[option].lower() + "...")

def assignmentsFilter(dateString, config):
    today = dateString
    scheduleData = getSchedule()
    dates = scheduleData["list"]
    courseData = scheduleData["dictionary"]
    if scheduleCheck(today, dates):
        assignment = courseData[today]
        print("\n\tThere's an assignment today:  ")
        print("\t\tFor {}, in week {}".format(today, assignment["Week"]))
        for key in sorted(assignment.keys()):
            if key not in ["Date", "Week", "Class", "Day"]:
                print("\t\t", key + ":  ", assignment[key])
        response = input("\n\tWould you like to create a file for this assignment ('N' = 'no', 'Y' = 'yes'):  ")
        if response.upper() in ["Y", "YES"] and len(response) > 0:
            print("\t\tOkay, we'll create a file named:  ch{}.".format(assignment["Chapter"].lower()))
    else:
        print("\n\t\tThere are no assignment today.")
    actionGet(addOption(OPTIONS, "QUIT"))

def buildChoicesForFiles(listOfFiles):
    choices = {}
    folderChoices = {}
    folderIndex = 1
    for folder, files in listOfFiles.items():
        if len(files) > 0
            folderChoices[folderIndex] = folder
            fileChoices = {}
            fileIndex = 1
            for file in files:
                fileChoices[fileIndex] = file
            choices[folderIndex] = fileChoices
        folderIndex += 1
    if len(folderChoices.keys()) == 1:
        print("\n\tThe only directory that has files is: ", folderChoices[1])
        printOptions(choices[1])
    else:
        print()

    return choices

def main():
    config = configGet()
    # webbrowser.open('file://' + os.path.realpath(FILENAME))
    today = getDate()
    # today = "2019-11-21"
    print("\n\tGreat {}!  Today's date is {}.".format(config["firstName"], today))
    assignmentsFilter(today, config)


main()
