import csv
from datetime import datetime

SCHEDULE = 'schedule.csv'
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

# A function that opens a CSV file to create and return a date-based list and
# dictionary.
def getSchedule(filename):
    with open(filename) as csv_file:
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
                dateList = row[0].split("/")
                # SEE:  https://docs.python.org/3/library/datetime.html?highlight=datetime#module-datetime
                # Given:  MM/DD/YYYY, Required:  YYYY-MM-DD
                mm = str(dateList[0]).zfill(2)
                dd = str(dateList[1]).zfill(2)
                dateString = "-".join([dateList[2], mm , dd])
                dates.append(dateString)
                datesDictionary[dateString] = rowDictionary
                line_count += 1
        return {"list": dates, "dictionary": datesDictionary}


def scheduleCheck(date=getDate(), dates=[]):
    try:
        if dates.index(date) >= 0:
            return True
    except ValueError:
        return False
