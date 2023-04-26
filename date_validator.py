 
import datetime
import math

"""
Martin Luther King Jr. Fay
Occurs on the Third Monday in January
"""
def mlk(date):
    month = 1
    day = 1
    year = date.year()
    days_to_third_monday=((1 - datetime.date(date.year, month, day).weekday()) % 7) + 14

    return datetime.date(year, month, day) + datetime.timedelta(days=days_to_third_monday)

"""
President's Day
Occurs on the Third Monday in February
"""
def presidents(date):
    month = 2
    day = 1
    year = date.year()
    days_to_third_monday=((1 - datetime.date(date.year, month, day).weekday()) % 7) + 14

    return datetime.date(year, month, day) + datetime.timedelta(days=days_to_third_monday)

"""
Good Friday
Occurs on the Friday right before Easter
Easter occurs on the First Sunday after the Paschal Full Moon
We will use the Gauss Easter Algorithm
"""
def good_friday():
    year = date.year()
    days_to_third_monday=((1 - datetime.date(date.year, month, day).weekday()) % 7) + 14

    return datetime.date(year, month, day) + datetime.timedelta(days=days_to_third_monday)

    A = year % 19 # Year in Metonic Cycle
    B = year  % 4 # Number of leap days Julia's Calendar
    C = year % 7 # Non-leap years have one day longer than 52 weeks
     
    P = math.floor(year / 100)
    Q = math.floor((13 + 8 * P) / 25)
    M = (15 - Q + P - P // 4) % 30
    N = (4 + P - P // 4) % 7 # Difference in # leap days Julian and Gregorian
    D = (19 * A + M) % 30 # Date of Paschal Full Moon in refernce to 3/21
    E = (2 * B + 4 * C + 6 * D + N) % 7  # # of days from Paschal full moon to next Sunday
    days = (22 + D + E)
  
    # when D is 29
    if ((D == 29) and (E == 6)):
        return datetime.date(year, 4, 19)
    
    # when D is 28
    elif ((D == 28) and (E == 6)):
        return datetime.date(year, 4, 18)
     
    else:     
        # Move to April
        if (days > 31):
            return datetime.date(year, 4, (days - 31))
        # Stay in March
        else:
 
            return datetime.date(year, 3, days)

"""
Memorial Day
Occurs on the Last Monday in May
"""
def memorial(date):
    month = 5
    day = 31
    year = date.year()
    days_to_last_monday= datetime.date(date.year, month, day).weekday()

    return datetime.date(year, month, day) - datetime.timedelta(days=days_to_last_monday)

"""
Labor Day
Occurs on the First Monday in September
"""
def labor(date):
    month = 9
    day = 1
    year = date.year()
    days_to_first_monday= (1 - datetime.date(date.year, month, day).weekday()) % 7

    return datetime.date(year, month, day) + datetime.timedelta(days=days_to_first_monday)



"""
Thanksgiving
Occurs on the Fourth Thursday in November
Note: Can be five Thursdays so not always the last Thursday
"""
def thanksgiving():
    month = 11
    day = 1
    year = date.year()
    days_to_fourth_thursday= ((3 - datetime.date(date.year, month, day).weekday()) % 7) + 21

    return datetime.date(year, month, day) + datetime.timedelta(days=days_to_fourth_thursday)


#Returns True if the given date is a common holiday, False otherwise
def is_common_holiday(date):  
    
    # Holidays with unchanging dates
    holidays = [
        datetime.date(date.year, 1, 1),   # New Year's Day
        datetime.date(date.year, 6, 19),  #Juneteenth
        datetime.date(date.year, 7, 4),   # Independence Day
        datetime.date(date.year, 12, 25), # Christmas Day
    ]
    holidays.append(mlk(date))
    holidays.append(presidents(date))
    holidays.append(good_friday(date))
    holidays.append(memorial(date))
    holidays.append(labor(date))
    holidays.append(thanksgiving(date))
    
    return date in holidays

def date_config(option,month,day,year):
    now = datetime.datetime.now()
    today = now.date()


    if ((month == "") and (day == "") and (year == "")):
        month = today.month
        day = today.day
        year = today.year
    elif ((month == "") or (day == "") or (year == "")):
        if (month == ""):
            print("Missing month entry for" ,option)
        if (day == ""):
            print("Missing day entry for" ,option)
        if (year == ""):
            print("Missing year entry for" ,option)
        return False
    else:
        month = int(month)
        year = int(year)
        day = int(day)
        if not 1 <= month <= 12:
            print("Invalid month entry for <{}> please input an integer in the range 1-12".format(option))
            return False

        if not 1 <= year <= today.year:
            print("Invalid year entry for <{}> please input a year before or equal to this year".format(option))
            return False
        if (year == today.year):
            if (month > today.month):
                print("Invalid month entry for <{}> please input a month before or equal to this month".format(option))
                return False
            if (month == today.month):
                if (day >= today.day):
                    print("Invalid date entry for <{}> please input a date before today of this month".format(option))
                    return False

        try:
            date = datetime.datetime(year, month, day)
        except ValueError:
            print("Invalid date entry for <{}> please input a valid date for the month: {}".format(option,month))
            return False

        if (date.weekday() >=5):
            print("Invalid date entry for <{}>\nPlease input a valid date during the week".format(option))
            return False
        elif is_common_holiday(date):
            print("Invalid date entry for <{}>\nPlease input a valid date that is not a holiday.".format(option))
            return False
    
    return True