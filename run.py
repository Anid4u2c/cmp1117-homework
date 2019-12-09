from calendar import getDate, getSchedule, scheduleCheck
from config import configGet
from fileActions import fileCreate, fileNameGet, fileRename, filesList, OPTIONS_FILE, SUBFOLDERS
from helpers import addOption, printOptions

OPTIONS_NAME = {1: "Allow the application to name the file for you.", 2: "Specify a name for your file."}
OPTIONS = {1: "Create a file for an assignment", 2: "List all assignment files", 3: "Rename a assignment file"}

def actionGet(options):
    option = printOptions(options)
    while option != len(OPTIONS.keys()):
        print("\n\t Okay, let's " + OPTIONS[option].lower() + "...")
        if option == 1:
            fileType = printOptions(addOption(OPTIONS_FILE, "GO BACK"))
            while fileType != len(OPTIONS_FILE.keys()):
                fileNameOption = printOptions(addOption(OPTIONS_NAME, "GO BACK"))
                while fileNameOption != len(OPTIONS_NAME.keys()):
                    if fileNameOption == 2:
                        fileName = input("\n\tWhat would you like to name your '{}' file?  ".format(OPTIONS_FILE[fileType]))
                    else:
                        fileName = fileNameGet(OPTIONS_FILE[fileType])
                    fileCreate(fileName, OPTIONS_FILE[fileType])
                fileType = len(OPTIONS_FILE)
            actionGet(options)
        elif option == 2:
            filesList(SUBFOLDERS)
            print("\n\t\tFinished " + fileType.lower() + ".")
            actionGet(options)
        elif option == 3:
            filesByFolder = filesList(SUBFOLDERS)
            for folder, files in filesByFolder.items():
                renamingOpts = buildChoicesForFiles({folder:files})
                if len(renamingOpts.keys()) >= 1:
                    for key, fileOpts in renamingOpts.items():
                        fileType = OPTIONS_FILE[key]
                        print("\n\tPick which '{}' file to rename:".format(fileType))
                        oldName = fileOpts[printOptions(addOption(fileOpts, "GO BACK"))]
                        while oldName != "GO BACK":
                            fileNameOption = printOptions(addOption(OPTIONS_NAME, "GO BACK"))
                            while fileNameOption != len(OPTIONS_NAME.keys()):
                                if fileNameOption == 2:
                                    newName = input("\n\tWhat would you like to rename your {} file?  ".format(fileType))
                                else:
                                    newName = fileNameGet(fileType)
                                fileRename(oldName, newName, fileType)
                                fileNameOption = len(OPTIONS_NAME.keys())
                            oldName = "GO BACK"
                    actionGet(options)
                        #printOptions(addOption(renamingOpts, "GO BACK"))
                else:
                    print("\n\t\tNo files to rename in directory:  {}".format(folder))
            actionGet(options)
        #print("\n\t\tOkay, let's " + OPTIONS[option].lower() + "...")

def assignmentsFilter(dateString, config):
    today = dateString
    today = "2019-11-21"
    scheduleData = getSchedule()
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
            response = input("\n\tWould you like to create a file for today's "
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
        choices[folderIndex] = fileChoices
        folderIndex += 1
    return choices

def main():
    config = configGet()
    # webbrowser.open('file://' + os.path.realpath(FILENAME))
    today = getDate()
    # today = "2019-11-21"
    print("\n Great {}!  Today's date is {}.".format(config["firstName"], today))
    assignmentsFilter(today, config)

main()
