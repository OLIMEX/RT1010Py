from machine import RTC

rtc = RTC()

# get date and time
#   return Tuple (Year, Month, Day, Day-of-Week, Hour, Minute, Seconds, ms)
#   weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
#
print( rtc.datetime() )
