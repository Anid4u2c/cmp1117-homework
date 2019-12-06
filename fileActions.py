import os
import sys
from os import path

from calendar import getDate, getDateMANUAL, OPTIONS_DATE
from helpers import printOptions

BASEPATH = "assignments"
OPTIONS_FILE = {1: "homework", 2: "labs", 3: "case study", 4: "GO BACK"}

def fileCreate(name, type):
    # detect the current working directory and print it
    pathStr = os.getcwd()
    print("\r\n\tThe current working directory is %s" % pathStr)
    pathStr = os.path.join(os.getcwd(), BASEPATH, type, name)
    try:
        if path.exists(pathStr):
            print("\r\n\tFile already exists!")
        else:
            file = open(pathStr, "w")
    except FileNotFoundError:
        print("\r\n\tFileNotFoundError:  Creation of the file '%s' failed" % name)
        folderCreate(type)
        fileCreate(name, type)
    except OSError:
        print("\r\n\tOSError:  Creation of the file '%s' failed" % name)
        folderCreate(type)
        fileCreate(name, type)
    else:
        print("\r\n\tSuccessfully created the file '%s' " % name)

# SEE:  https://code-maven.com/listing-a-directory-using-python
def filesList(dir):
    path = '.'
    path = os.path.join(os.getcwd(), BASEPATH, dir)

    if len(sys.argv) == 2:
        path = sys.argv[1]

    files = os.listdir(path)
    if len(files) > 0:
        print("\t\tDIRECTORY:  " + dir)
        for name in files:
            print("\t\t\t" + name)
    #except FileNotFoundError:
    return

def fileNameGet(fileType):
    try:
        chapter = int(input("\r\n\tWhat chapter is the {} file for?  ".format(fileType)))
        exercise = int(input("\r\n\tWhat exercise is the {} file for?  ".format(fileType)))
        dateOption = printOptions(OPTIONS_DATE)
        if dateOption == 1:
            dateString = getDateMANUAL()
        else:
            dateString = getDate()
        chapter = str(chapter).zfill(2)
        exercise = str(exercise).zfill(2)
        if chapter == "00" or exercise == "00":
            print("\r\n\t\tERROR:  Please enter the proper information.")
            fileNameGet(fileType)
    except ValueError:
        print("\r\n\t\tERROR:  Please enter a number for the Chapter and Excercise.")
        fileNameGet(fileType)
    return "ch" + chapter + ".ex" + exercise + "." + dateString + ".py"

def fileRename(oldName, newName):
    return

# SEE:  https://stackabuse.com/creating-and-deleting-directories-with-python/
def folderCreate(name):
    if path.exists(os.path.join(os.getcwd(), BASEPATH)):
        print("\r\n\tCreating folder named:", name)
        # detect the current working directory and print it
        pathStr = os.getcwd()
        print("\r\n\t\tIn the current working directory is %s" % pathStr)
        pathStr = os.path.join(os.getcwd(), BASEPATH, name)
        try:
            if path.exists(pathStr):
                print("\r\n\tFolder named '{}' already exists!".format(name))
            else:
                os.mkdir(pathStr)
        except OSError:
            print("\r\n\tOSError:  Creation of the directory %s failed" % pathStr)
        else:
            print("\r\n\tSuccessfully created the directory:  %s " % pathStr)
    else:
        print("\r\n\tCreating '{}' folder for the first time.".format(BASEPATH))
        os.mkdir(os.path.join(os.getcwd(), BASEPATH))
        folderCreate(name)

def foldersCreate(folders):
    for folder in folders:
        folderCreate(folder)

