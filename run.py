from calendar import getDate, getSchedule, scheduleCheck
from config import configGet

def assignmentsFilter(dateString, config):
    today = dateString
    scheduleData = getSchedule()
    dates = scheduleData["list"]
    courseData = scheduleData["dictionary"]
    if scheduleCheck(today, dates) == True:
        assignment = courseData[today]
        print("\r\n\tThere's an assignment today:  ")
        print("\t\tFor {}, in week {}".format(today, assignment["Week"]))
        for key in sorted(assignment.keys()):
            if key not in ["Date", "Week", "Class", "Day"]:
                print("\t\t", key + ":  ", assignment[key])
        response = input("\r\n\tWould you like to create a file for this assignment ('N' = 'no', 'Y' = 'yes'):  ")
        if response.upper() == "Y" and len(response) > 0:
            print("\t\tOkay, we'll create a file named:  ch{}.".format(assignment["Chapter"].lower()))

    else:
        print("\r\n\tThere's no assignment today...")

def main():
    config = configGet()
    # webbrowser.open('file://' + os.path.realpath(FILENAME))
    today = getDate()
    #today = "2019-11-21"
    print("\r\n\tGreat {}!  Today's date is {}...".format(config["firstName"], today))
    assignmentsFilter(today, config)


main()
