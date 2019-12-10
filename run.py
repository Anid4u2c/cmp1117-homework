from calendar import getDate, getSchedule, scheduleCheck
from config import configGet, configEdit
from fileActions import fileCreate, fileNameGet, fileRename, filesList, OPTIONS_FILE, SUBFOLDERS
from helpers import addOption, printOptions

OPTIONS_NAME = {1: "Allow the application to name the file for you.", 2: "Specify a name for your file."}
OPTIONS = {1:"Create a file for an assignment", 2:"List all assignment files",
           3:"Rename a assignment file", 4:"Edit your configuration"}

def actionGet(options):
    option = printOptions(options)
    while option != len(OPTIONS.keys()):
        print("\n\t Okay, let's " + OPTIONS[option].lower() + "...")
        if option == 1:
            fileInt = printOptions(addOption(OPTIONS_FILE, "GO BACK"))
            fileType = OPTIONS_FILE[fileInt]
            while fileInt != len(OPTIONS_FILE.keys()):
                fileNameOption = printOptions(addOption(OPTIONS_NAME, "GO BACK"))
                while fileNameOption != len(OPTIONS_NAME.keys()):
                    if fileNameOption == 2:
                        fileName = input("\n\tWhat would you like to name your '{}' file?  ".format(fileType))
                    else:
                        fileName = fileNameGet(fileType)
                    fileCreate(fileName, fileType)
                    fileNameOption = len(OPTIONS_NAME.keys())
                fileInt = len(OPTIONS_FILE)
            actionGet(options)
        elif option == 2:
            filesList(SUBFOLDERS)
        elif option == 3:
            filesByFolder = filesList(SUBFOLDERS)
            folderOpts, fileOpts = buildChoicesForFiles(filesByFolder)
            processChoicesForFiles(folderOpts, fileOpts)
        elif option == 4:
            configEdit()
        actionGet(options)

def assignmentsFilter(dateString, config):
    today = dateString
    #today = "2019-11-21"
    scheduleData = getSchedule()
    '''
    for date, assignmentData in scheduleData["dictionary"].items():
        #printOptions(buildChoicesForFiles({date:assignmentData}))
        print("date:  ", date, "assignment:  ", assignmentData)
    '''
    dates = scheduleData["list"]
    courseData = scheduleData["dictionary"]
    if scheduleCheck(today, dates):
        assignment = courseData[today]
        print("\n\tThere's an assignment on {}, in week {}".format(today,assignment["Week"]))
        assignmentOpts = {}
        assignmentMap = {}
        index = 1
        for key in sorted(assignment.keys()):
            if key not in ["Date", "Week", "Class", "Day"]:
                print("\t\t", key + ":  ", assignment[key])
            if key in ["Lab", "Homework"]:
                assignmentMap[index] = key
                assignmentOpts[index] = assignment[key]
                index += 1
        for key, value in assignmentOpts.items():
            fileType = assignmentMap[key].lower()
            response = input("\n Would you like to create a file for today's "
                             "'{}' assignment ('Y' = 'Yes'):  ".format(fileType))
            if response.upper() in ["Y", "YES"] and len(response) > 0:
                fileNameOption = printOptions(
                    addOption(OPTIONS_NAME, "GO BACK"))
                while fileNameOption != len(OPTIONS_NAME.keys()):
                    if fileNameOption == 2:
                        fileName = input(
                            "\n\tWhat would you like to name your {} "
                            "file?  ".format(fileType))
                    else:
                        if fileType == "lab":
                            fileTypeName = assignment["Lab"].lower()
                        elif fileType == "Homework":
                            fileTypeName = assignment["Homework"].lower()
                        else:
                            fileTypeName = "assignment"
                        fileName = "ch{}.{}.{}.py".format(assignment["Chapter"], fileTypeName, today)
                    fileCreate(fileName, fileType)
                    fileNameOption = len(OPTIONS_NAME.keys())
    else:
        print("\n\t\tThere are no assignment today.")
    actionGet(addOption(OPTIONS, "QUIT"))

def buildChoicesForFiles(listOfFiles):
    choices = {}
    folderChoices = {}
    folderIndex = 1
    for folder, files in listOfFiles.items():
        fileChoices = {}
        if len(files) > 0:
            folderChoices[folderIndex] = folder
            fileIndex = 1
            for file in files:
                fileChoices[fileIndex] = file
                fileIndex += 1
        choices[folderIndex] = fileChoices
        folderIndex += 1
    return folderChoices, choices

def processChoicesForFiles(folderOpts, fileOpts):
    if len(folderOpts.keys()) >= 1:
        print("\n Pick which type of file to rename:  ")
        folderChoice = printOptions(addOption(folderOpts, "GO BACK"))
        while folderChoice != len(folderOpts.keys()):
            files = fileOpts[folderChoice]
            fileType = folderOpts[folderChoice]
            fileChoice = printOptions(addOption(files, "GO BACK"))
            while fileChoice != len(files.keys()):
                oldName = files[fileChoice]
                fileNameOption = printOptions(addOption(OPTIONS_NAME, "GO BACK"))
                while fileNameOption != len(OPTIONS_NAME.keys()):
                    if fileNameOption == 2:
                        newName = input(
                            "\n\tWhat would you like to rename your {} "
                            "file?  ".format(fileType))
                    else:
                        newName = fileNameGet(fileType)
                    fileRename(oldName, newName, fileType)
                    fileNameOption = len(OPTIONS_NAME.keys())
                fileChoice = len(files.keys())
            folderChoice = len(folderOpts.keys())
    else:
        print("\n\t\tNo files to rename in directory.")
    return

def main():
    config = configGet()
    # webbrowser.open('file://' + os.path.realpath(FILENAME))
    today = getDate()
    # today = "2019-11-21"
    print("\n Great {}!  Today's date is {}.".format(config["firstName"], today))
    assignmentsFilter(today, config)

main()
