def printOptions(options):
    print("\n\tHere are your options:")
    for key in options.keys():
        print("\t\t{} : {}".format(key, options [key]))
    try:
        choice = int(input("\n\tWhich option do you choose?  "))
        if choice in options.keys():
            return choice
        else:
            print("\n\t\tERROR: Must be in the list of options (1-{}).".format(len(options.keys())))
    except ValueError:
        print("\n\t\tValueError: Response cannot be empty, and must be type: 'int'.")
        printOptions(options)

def addOption(dictionary, option):
    if option is None:
        dictionary = {}
    key = len(dictionary.keys())+1
    if option not in dictionary.values():
        dictionary[key] = option
    return dictionary
