import json

from calendar import getDateTime

FILENAME = ".config"
FOLDERS = ("homework", "labs")
KEY_MAP = {"firstName": "First Name", "lastName": "Last Name",
           "studentId": "Student ID", "dateTime": "Last Updated"}
TEMPLATE = ("dateTime", "files", "firstName", "lastName", "studentId")

def configEdit():
    return configSet(configOutput(userDataGet()))


def configGet():
    print("\n Checking current folder for '.config' file...")
    try:
        configFile = open(FILENAME, "r")
        config = json.loads(configFile.read())
        print("\n\tConfiguration file found.")
        configFile.close()
    except IOError:
        print("\n\tNo configuration file found.")
        config = configSet(userDataGet())
    #return configEdit(configOutput(config))
    return configOutput(config)



def configOutput(config):
    try:
        output = "\n\tHere is the current configuration for this program:\n"
        for key in config.keys():
            if key not in ["dateTime", "files"]:
                output += "\n\t{}:  {}".format(mapKey(key), config[key])
        return config
    except AttributeError:
        isConfigGood = keyCheck(config, TEMPLATE)
        if isConfigGood == False:
            print("\n\tThe file does not contain the proper configuration...")
            print("\n\tisConfigGood:  ", isConfigGood)
            return userDataGet()
        else:
            return config

def configSet(config):
    print("\n\tSetting or updating the user configuration for this program:\n")
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
    firstName = input('\n\tEnter your first name: ')
    lastName = input('\n\tEnter your last name: ')
    studentId = input('\n\tEnter your student ID: ')
    config = {"dateTime": getDateTime(), "firstName": firstName, "lastName": lastName, "studentId": studentId}
    return config
