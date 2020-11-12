import datetime 
import numpy

def parse_datetime(string):
    (month, day, remainder) = string.split('/')
    (year, time) = remainder.split(' ')
    (hour, minute) = time.split(':')
    return datetime.datetime(
        int(year) + 2000, 
        int(month),
        int(day),
        int(hour),
        int(minute)
    )

# credits to https://matthew-brett.github.io/teaching/smoothing_intro.html
def fwhm2sigma(fwhm):
    return fwhm / numpy.sqrt(8 * numpy.log(2))

# credits to https://matthew-brett.github.io/teaching/smoothing_intro.html
def sigma2fwhm(sigma):
    return sigma * numpy.sqrt(8 * numpy.log(2))