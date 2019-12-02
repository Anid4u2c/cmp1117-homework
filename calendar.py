import csv
from datetime import datetime

HEADERS = (
    "Date", "Week", "Class", "Day", "Learning Outcome", "Chapter", "Pages", "Quiz", "Assignmt", "Lab", "Outcomes")
OPTIONS_DATE = {1: "Specify a specific date", 2: "Use today's date"}

def getDate():
    # Determine current date and time of the device used.
    now = datetime.now()

    # Display date in the format
    return now.strftime('%Y-%m-%d')

def getDateMANUAL():
    print("\r\n\t\tHINT:  Use the due date of the assignment.")
    year = input("\r\n\tEnter the year (YYYY):  ")
    month = input("\r\n\tEnter the month (MM):  ")
    day = input("\r\n\tEnter the day (DD):  ")
    if len(day) != 2 or len(month) != 2 or len(year) != 4:
        print("\r\n\t\tERROR:  Please enter the proper number of characters.")
        getDateMANUAL()
    else:
        return "-".join([year, month, day])


def getDateTime():
    # Determine current date and time of the device used.
    now = datetime.now()

    # Display date and time in the format: YYYY-MM-DD H:M:S
    dateTime = now.strftime('%Y-%m-%d %H:%M:%S')
    return dateTime


def getSchedule():
    with open('schedule.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        dates = []
        datesDictionary = {}
        headers = ""
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                headers = row
                # print(headers)
                line_count += 1
            else:
                rowDictionary = {}
                for index in range(len(row)):
                    cell = row[index]
                    if len(cell) > 0:
                        rowDictionary[headers[index]] = cell

                # Date,Week,Class,Day,Learning Outcome,Chapter,Pages,Quiz,Assignmt,Lab,Outcomes
                # print(f'\tDate: {row[0]}, Learning Outcome:  {row[4]} from Chapter {row[5]}.')

                dateList = row[0].split("/")
                # SEE:  https://docs.python.org/3/library/datetime.html?highlight=datetime#module-datetime
                # Given:  MM/DD/YYYY, Required:  YYYY-MM-DD
                dateString = "-".join([dateList[2], dateList[0], dateList[1]])
                dates.append(dateString)
                datesDictionary[dateString] = rowDictionary
                line_count += 1
        # print(f'Processed {line_count} lines.')
        # print(dates)
        # print(datesDictionary)
        # print(dates.index(getDate()))
        return {"list": dates, "dictionary": datesDictionary}


def scheduleCheck(date=getDate(), dates=[]):
    try:
        if dates.index(date) >= 0:
            return True
    except ValueError:
        return False
