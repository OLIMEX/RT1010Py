from machine import RTC

rtc = RTC()
# set a specific date and time
#   Year, Month, Day, Day-of-Week, Hour, Minute, Seconds, ms
rtc.datetime((2017, 8, 23, 1, 12, 48, 0, 0)) 

print( rtc.datetime() ) # get date and time
