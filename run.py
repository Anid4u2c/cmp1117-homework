from calendar import getDate, getSchedule, scheduleCheck, SCHEDULE
from config import configGet, configEdit
from fileActions import fileCreate, fileNameGet, fileRename, filesList, OPTIONS_FILE, SUBFOLDERS
from helpers import addOption, printOptions

OPTIONS_NAME = {1: "Allow the application to name the file for you.", 2: "Specify a name for your file."}
OPTIONS = {1:"Create a file for an assignment", 2:"List all assignment files",
           3:"Rename a assignment file", 4:"Edit your configuration"}
SCHEDULE_DATA = getSchedule(SCHEDULE)

# A function that gets the allows the user to choose from the main 'OPTIONS',
# and then performs the selected action.
def actionGet(options):
    option = printOptions(options)
    while option != len(OPTIONS.keys()):
        print("\n\t Okay, let's " + OPTIONS[option].lower() + "...")
        if option == 1:
            response = input("\n Would you like to create a file for a "
                             "specific date ('Y' = 'Yes'):  ")
            if response.upper() in ["Y", "YES"]:
                dateOpts, assignmentOpts = buildChoicesForDates(
                    SCHEDULE_DATA['dictionary'])
                dateString = processChoicesForDates(dateOpts)
                while dateString != len(dateOpts.keys()):
                    assignmentsFilter(dateString)
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

# A function that receives a date string in the format of YYYY-MM-DD.
# The function filters through the dates and assignment data, and
# notifies the user if there is an assignment
def assignmentsFilter(dateString):
    today = dateString
    dates = SCHEDULE_DATA["list"]
    courseData = SCHEDULE_DATA["dictionary"]
    if scheduleCheck(today, dates):
        assignment = courseData[today]
        print("\n\tThere's assignment data for {}, in week {}"
              .format(today,assignment["Week"]))
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
            response = input("\n Would you like to create a file for this "
                             "'{}' assignment ('Y' = 'Yes'):  ".format(fileType))
            if fileType == "lab":
                fileType += "s"
            if response.upper() in ["Y", "YES"] and len(response) > 0:
                fileNameOption = printOptions(
                    addOption(OPTIONS_NAME, "GO BACK"))
                while fileNameOption != len(OPTIONS_NAME.keys()):
                    if fileNameOption == 2:
                        fileName = input(
                            "\n\tWhat would you like to name your {} "
                            "file?  ".format(fileType))
                    else:
                        if fileType.lower() in ["lab", "labs"]:
                            fileTypeName = assignment["Lab"].lower()
                        elif fileType == "Homework":
                            fileTypeName = assignment["Homework"].lower()
                        else:
                            fileTypeName = "assignment"
                        fileName = "ch{}.{}.{}.py".format(assignment["Chapter"], fileTypeName, today)
                    fileCreate(fileName, fileType)
                    fileNameOption = len(OPTIONS_NAME.keys())
    else:
        dateOpts, assignmentOpts = buildChoicesForDates(
            SCHEDULE_DATA['dictionary'])
        while today is not None:
            print("\n\t\tThere's no assignment data for {}".format(today))
            response = input("\n Would you like to create a file for a "
                             "different date ('Y' = 'Yes'):  ")
            if response.upper() in ["Y", "YES"]:
                dateString = processChoicesForDates(dateOpts)
                assignmentsFilter(dateString)
    actionGet(addOption(OPTIONS, "QUIT"))

# A function that returns choices for dates and assignments.  'dateChoices'
# contains a list of assignment dates.  'choices' contain a dictionary that
# can be used to get the date-based assignment options.
def buildChoicesForDates(listOfAssignments):
    choices = {}
    dateChoices = {}
    dateIndex = 1
    for date, assignment in listOfAssignments.items():
        assignChoices = {}
        dateChoices[dateIndex] = date
        assignIndex = 1
        for key in assignment:
            if key in ["Homework", "Lab"]:
                assignChoices[assignIndex] = assignment[key].lower()
                assignIndex += 1
        if len(assignChoices.keys()) > 0:
            choices[dateIndex] = assignChoices
            dateIndex += 1
        else:
            dateChoices.pop(dateIndex)
    return dateChoices, choices

# A function that returns choices for folders and files.  'folderChoices'
# contains a list of folders that are not empty.  'choices' contain
# a dictionary that can be used to get the folder-based file options.
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

# A function that receives dictionaries of choices, for dates
# whose assignment choices contain values for the keys:  'Homework' or 'Labs'.
def processChoicesForDates(dateOpts):
    print("\n For which date would you like to create an assignment file:  ")
    dateChoice = printOptions(addOption(dateOpts, "GO BACK"))
    while dateChoice != len(dateOpts.keys()):
        dateString = dateOpts[dateChoice]
        assignmentsFilter(dateString)



# A function that receives dictionaries of choices, for folders and files.
# The function filters through files and only returns options for folders
# that contain files.
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
            folderChoice = printOptions(folderOpts)
    else:
        print("\n\t\tNo files to rename in directory.")

def main():
    config = configGet()
    today = getDate()
    print("\n Great {}!  Today's date is {}.".format(config["firstName"], today))
    assignmentsFilter(today)

main()
