import json

from calendar import getDate, getDateTime, getSchedule, scheduleCheck

FILENAME = ".config"
KEY_MAP = {"firstName": "First Name", "lastName": "Last Name",
           "studentId": "Student ID", "dateTime": "Last Updated"}
TEMPLATE = ("dateTime", "firstName", "lastName", "studentId")


def configEdit(config):
    response = input("\r\n\tWould you like to edit the current configuration (N = 'No', Y = 'Yes'):  ")
    if response.upper() == "Y" and len(response) > 0:
        return configSet(configOutput(userDataGet()))
    else:
        return config


def configGet():
    print("\r\n\tChecking current folder for '.config' file...\r\n")
    try:
        configFile = open(FILENAME, "r")
        config = json.loads(configFile.read())
        print("\r\n\t\tConfiguration file found.\r\n")
        configFile.close()
    except IOError:
        print("\r\n\t\tNo configuration file found.\r\n")
        config = configSet(userDataGet())
    return configEdit(configOutput(config))


def configOutput(config):
    try:
        output = "\r\n\tHere is the current configuration for this program:\r\n"
        for key in config.keys():
            if key != "dateTime":
                output += "\r\n\t{}:  {}".format(mapKey(key), config[key])
        return config
    except AttributeError:
        isConfigGood = keyCheck(config, TEMPLATE)
        if isConfigGood == False:
            print("\r\n\tThe file does not contain the proper configuration...")
            print("\r\n\tisConfigGood:  ", isConfigGood)
            return userDataGet()
        else:
            return config


def configSet(config):
    print("\r\n\tSetting or updating the user configuration for this program:\r\n")
    file = open(FILENAME, "w")
    # config += "dateTime:  " + config["dateTime"] + "\n"
    # config += "firstName:  " + config["firstName"] + "\n"
    # config += "lastName:  " + config["lastName"] + "\n"
    # config += "studentId:  " + config["studentId"] + "\n"
    file.write(json.dumps(config))
    file.close()

    return config


def keyCheck(dictionary, template):
    try:
        success = False
        for key in dictionary.keys():
            if template.index(key) >= 0:
                success = True
            else:
                success = False
        return success
    except AttributeError:
        return False


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

def mapKey(key):
    try:
        value = KEY_MAP[key]
    except KeyError:
        value = key
    return value

def userDataGet():
    firstName = input('\r\n\tEnter your first name: ')
    lastName = input('\r\n\tEnter your last name: ')
    studentId = input('\r\n\tEnter your student ID: ')
    config = {"dateTime": getDateTime(), "firstName": firstName, "lastName": lastName, "studentId": studentId}
    return config


main()
