from calendar import getDate, getSchedule, scheduleCheck
from config import configGet


def main():
    config = configGet()
    today = getDate()
    today = "2019-11-21"
    # print(config)
    print("\r\n\tGreat {}!  Today's date is {}...".format(config["firstName"], today))
    # webbrowser.open('file://' + os.path.realpath(FILENAME))
    scheduleData = getSchedule()
    dates = scheduleData["list"]
    courseData = scheduleData["dictionary"]
    if scheduleCheck(today, dates) == True:
        assignment = courseData[today]
        print("\r\n\tThere's an assignment today:  ")
        for key in assignment.keys():
            print("\t\tkey:  ", key, ", value:  {}".format(assignment[key]))
    else:
        print("\r\n\tThere's no assignment today...")

main()
