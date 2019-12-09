import os
import sys
from os import path

from calendar import getDate, getDateMANUAL, OPTIONS_DATE
from helpers import printOptions

BASEPATH = "assignments"
OPTIONS_FILE = {1: "homework", 2: "labs", 3: "case study"}
SUBFOLDERS = tuple(OPTIONS_FILE.values())

def fileCreate(name, type):
    if type(type) == 'int' and type in OPTIONS_FILE.keys():
        type = OPTIONS_FILE[type]
    fileExists = False
    # detect the current working directory and print it
    pathStr = os.getcwd()
    print("\n\tThe current working directory is %s" % pathStr)
    pathStr = os.path.join(os.getcwd(), BASEPATH, type, name)
    try:
        if path.exists(pathStr):
            fileExists = True
            print("\n\t\tATTENTION:  File already exists!")
        else:
            file = open(pathStr, "w")
    except FileNotFoundError:
        print("\n\tFileNotFoundError:  Creation of the file '%s' failed" % name)
        folderCreate(type)
        fileCreate(name, type)
    except OSError:
        print("\n\tOSError:  Creation of the file '%s' failed" % name)
        folderCreate(type)
        fileCreate(name, type)
    else:
        if fileExists == False:
            print("\n\t\tSUCCESS:  Created the file '%s' " % name)

# SEE:  https://code-maven.com/listing-a-directory-using-python
def filesList(directories):
    filesByFolder = {}
    pathStr = '.'
    for directory in directories:
        pathStr = os.path.join(os.getcwd(), BASEPATH, directory)

        if len(sys.argv) == 2:
            pathStr = sys.argv[1]

        try:
            # print("\n\tTrying to list the directory:  '{}'".format(directory))
            filesByFolder[directory] = []
            files = os.listdir(pathStr)
            if len(files) > 0:
                filesStr = ""
                for name in files:
                    filesStr += "\t\t\t↳ FILE:  " + name
                    filesByFolder[directory].append(name)
                print("\n\t\tDIRECTORY: ", directory, "has", len(filesByFolder[directory]), "files:")
                print(filesStr)
            else:
                print("\n\t\tDIRECTORY:  '{}' contains 0 files".format(directory))
        except FileNotFoundError:
            # print("\n\t\tThe directory:  '{}' does NOT exist...".format(directory))
            folderCreate(directory)
    return filesByFolder

def fileNameGet(fileType):
    try:
        if type(fileType) == 'int' and fileType in OPTIONS_FILE.keys():
            fileType = OPTIONS_FILE[fileType]
        chapter = int(input("\n\tWhat chapter is the {} file for?  ".format(fileType)))
        exercise = int(input("\n\tWhat exercise is the {} file for?  ".format(fileType)))
        dateOption = printOptions(OPTIONS_DATE)
        if dateOption == 1:
            dateString = getDateMANUAL()
        else:
            dateString = getDate()
        chapter = str(chapter).zfill(2)
        exercise = str(exercise).zfill(2)
        if chapter == "00" or exercise == "00":
            print("\n\t\tERROR:  Please enter the proper information.")
            fileNameGet(fileType)
    except ValueError:
        print("\n\t\tERROR:  Please enter a number for the Chapter and Excercise.")
        fileNameGet(fileType)
    return "ch" + chapter + ".ex" + exercise + "." + dateString + ".py"

def fileRename(oldName, newName, type):
    # detect the current working directory and print it
    pathStr = os.getcwd()
    print("\n\tThe current working directory is %s" % pathStr)
    newPathStr = os.path.join(os.getcwd(), BASEPATH, type, newName)
    oldPathStr = os.path.join(os.getcwd(), BASEPATH, type, oldName)
    try:
        if path.exists(newPathStr):
            print("\n\tFile with proposed name '{}', already exists!".format(newName))
        else:
            # SEE: https://www.tutorialspoint.com/python3/os_rename.htm
            os.rename(oldPathStr, newPathStr)
    except FileNotFoundError:
        print("\n\tFileNotFoundError:  Renaming of the file '%s' failed" % oldName)
    except OSError:
        print("\n\tOSError:  Renaming of the file '%s' failed" % oldName)
    else:
        print("\n\tSUCCESS:  Renamed the '{}' file from '{}' to '{}'".format(type, oldName, newName))

# SEE:  https://stackabuse.com/creating-and-deleting-directories-with-python/
def folderCreate(name):
    if path.exists(os.path.join(os.getcwd(), BASEPATH)):
        print("\n\tCreating folder named:", name)
        # detect the current working directory and print it
        pathStr = os.getcwd()
        print("\n\t\tIn the current working directory is %s" % pathStr)
        pathStr = os.path.join(os.getcwd(), BASEPATH, name)
        try:
            if path.exists(pathStr):
                print("\n\tFolder named '{}' already exists!".format(name))
            else:
                os.mkdir(pathStr)
        except OSError:
            print("\n\tOSError:  Creation of the directory %s failed" % pathStr)
        else:
            print("\n\tSuccessfully created the directory:  %s " % pathStr)
    else:
        print("\n\tCreating '{}' folder for the first time.".format(BASEPATH))
        os.mkdir(os.path.join(os.getcwd(), BASEPATH))
        folderCreate(name)

def foldersCreate(folders):
    for folder in folders:
        folderCreate(folder)

