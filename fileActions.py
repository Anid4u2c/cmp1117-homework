import os
import sys
from os import path

from calendar import getDate, getDateMANUAL, OPTIONS_DATE
from helpers import printOptions

BASEPATH = "assignments"
OPTIONS_FILE = {1: "homework", 2: "lab"}

def fileCreate(name, type):
    # detect the current working directory and print it
    path = os.getcwd()
    print("\r\n\tThe current working directory is %s" % path)
    path += "/" + BASEPATH + "/" + type + "/" + name
    try:
        if not fileExists(name):
            file = open(path, "x")
    except OSError:
        print("\r\n\tERROR:  Creation of the file '%s' failed" % path)
        path = os.getcwd() + "/" + BASEPATH + "/" + type
        folderCreate(type)
        fileCreate(name, type)
    else:
        print("\r\n\tSuccessfully created the file '%s' " % name)

# SEE:  https://www.guru99.com/python-check-if-file-exists.html
def fileExists(name):
    exists = False
    if path.isfile(name):
        exists = path.exists(name)
        print("file exist:" + str(exists))
    return exists

# SEE:  https://code-maven.com/listing-a-directory-using-python
def filesList(dir):
    path = '.'
    path = os.getcwd() + "/" + BASEPATH + "/" + dir + "/"

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
    if fileExists(oldName):
        return

# SEE:  https://stackabuse.com/creating-and-deleting-directories-with-python/
def folderCreate(name):
    # detect the current working directory and print it
    path = os.getcwd()
    print("\r\n\tThe current working directory is %s" % path)
    path += "/" + BASEPATH + "/" + name
    try:
        if not folderExists(name):
            os.mkdir(path)
    except OSError:
        print("\r\n\tERROR:  Creation of the directory %s failed" % path)
    else:
        print("\r\n\tSuccessfully created the directory:  %s " % path)

def foldersCreate(folders):
    for folder in folders:
        folderCreate(folder)

def folderExists(name):
    exists = False
    if path.isdir(name):
        exists = path.exists(name)
        print("\r\n\t\tDirectory '{}' exists:".format(name) + str(exists))
    else:
        print("\r\n\t\t'{}' is not a directory.".format(name))
    return exists


