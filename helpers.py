def printOptions(options):
    print("\r\n\tHere are your options:")
    for key in options .keys():
        print("\t\t{} : {}".format(key, options [key]))
    try:
        return int(input("\r\n\tWhich option do you choose?  "))
    except ValueError:
        print("\r\b\n\t\tERROR: Response cannot be empty, and must be in the list of options.")
        printOptions(options)
