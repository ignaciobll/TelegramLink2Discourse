import re
import requests
from lxml.html import fromstring

txt = """Ignacio Ballesteros, [13.09.17 15:36]\nPero es lo que voy a hacer vamos, si no funciona en alguno, mala suerte :(\n\nIgnacio Ballesteros, [13.09.17 15:49]\nLA REGEX DE VICTOR FUNCIONA\n\nDavid Mazarro, [13.09.17 15:51]\nPásala 😵\n\nRock Neurotiko, [13.09.17 15:52]\nhttp://.*\n\nDavid Mazarro, [13.09.17 15:52]\nlal\n\nIgnacio Ballesteros, [13.09.17 15:59]\nhttps://github.com/victorvillar/OldBot/blob/master/oldbot.py#L49"""


match_URL_re = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

is_URL = re.compile(match_URL_re)

# A config file is a key-value file separated by a space
correct_line = lambda line: len(line.strip(' ').strip('\n').split(' ')) == 2
config = {}
with open('link2discourse.conf', 'r') as conf:
    for line in conf.readlines():
        if correct_line(line):
            (k,v) = line.strip(' ').strip('\n').split(' ')
            config[k] = v

# We don't want to download everything (just check if exists)
def is_valid_URL(url):
    try:
        response = requests.head(url)
        return response.status_code < 400
    except:
        return False            

# Return only well formed AND valid urls
def match_URL(msg):
    link = is_URL.findall(msg)
    if link is not None:
        return [x for x in link if is_valid_URL(x)]
    else:
        None

def get_title(url):
    r = requests.get(url)
    tree = fromstring(r.content)
    return tree.findtext('.//title')

# f :: [URL] -> (Discourse Side Effect) :D
def post_urls_on_discourse(urls):
    title = get_title(urls[0])
    raw = "\n".join(urls)
    category = '4' # Staff by default
    url = "http://discourse.acmupm.es/posts"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"api_key\"\r\n\r\n " + config['token'] + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"api_username\"\r\n\r\n" + config['user']     + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"title\"\r\n\r\n" + title    + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"raw\"\r\n\r\n" + raw      + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"category\"\r\n\r\n" + category + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(title, str(response.status))

def process_msg(msg):
    urls = match_URL(msg)
    if urls is not None:
        post_urls_on_discourse(urls)
