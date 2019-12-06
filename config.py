import json

from calendar import getDateTime

FILENAME = ".config"
FOLDERS = ("homework", "labs")
KEY_MAP = {"firstName": "First Name", "lastName": "Last Name",
           "studentId": "Student ID", "dateTime": "Last Updated"}
TEMPLATE = ("dateTime", "files", "firstName", "lastName", "studentId")

def configEdit(config):
    response = input("\r\n\tWould you like to edit the current configuration ('Y' or 'Yes'):  ")
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
            if key not in ["dateTime", "files"]:
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
