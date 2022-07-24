import re

__url = None
__regexp = re.compile(r'https:\/\/youtu\.be\/\d*\w*|https:\/\/'
                      r'www\.youtube\.com\/watch\?v=\d*\w*|'
                      r'https:\/\/music.youtube\.com\/watch\?v=(?:\d*\w*-?\d*\w*|\d*\w*)*')


def validateUrl(url):
    __r = __regexp.search(url)
    if __regexp.match(url):
        global __url
        __url = __r.group(0)
        return True
    else:
        return False


def getValidatedUrl():
    return str(__url)