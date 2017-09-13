import re

match_URL_re = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

is_URL = re.compile(match_URL_re)

def match_URL(text):
    link = is_URL.match(text)
    if link is not None:
        
    else:
        return None
