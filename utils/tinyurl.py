import pyshorteners

def shorten_url(long_url):
    type_tiny = pyshorteners.Shortener()

    short_url = type_tiny.tinyurl.short(long_url)

    return short_url