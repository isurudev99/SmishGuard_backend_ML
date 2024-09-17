import pandas as pd
import re
import pickle

"""**Having IP Address:**"""
def having_ip_address(url):
    match = re.search(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  # IPv4
        r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)' # IPv4 in hexadecimal
        r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6

    if match:
        return 1
    else:
        return 0

"""**Abnormal URL**"""
from urllib.parse import urlparse
def abnormal_url(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    if match:
        return 1
    else:
        return 0

"""**Google index:**"""
from googlesearch import search
def google_index(url):
    site = search(url, 5)
    return 1 if site else 0

"""**Count Dot(.)**"""
def count_dot(url):
    count_dot = url.count('.')
    return count_dot

"""**Count www**"""
def count_www(url):
    return url.count('www')

"""**Count @**"""
def count_atrate(url):
    return url.count('@')

"""**Count dir:**"""
def count_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

"""**Count_embed_domain:**"""
def count_embed_domain(url):
    urldir = urlparse(url).path
    return urldir.count('//')

"""**Suspicious words in URL:**"""
def suspicious_words(url):
    match = re.search(r'PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr', url)
    if match:
        return 1
    else:
        return 0

"""**Short_URL**"""
def short_url(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0

"""**Count_https**"""

def count_https(url):
    return url.count('https')

"""**Count_http**"""

def count_http(url):
    return url.count('http')

"""**Count_%**"""

def count_per(url):
    return url.count('%')

"""**Count_?**"""

def count_ques(url):
    return url.count('?')

"""**Count_-**"""

def count_hyphen(url):
    return url.count('-')

"""**Count_=**"""

def count_equal(url):
    return url.count('=')

"""**URL_Length**"""

def url_length(url):
    return len(str(url))

"""**Hostname_length**"""

def hostname_length(url):
    return len(urlparse(url).netloc)

"""**First directory length**"""
from tld import get_tld
import os.path

def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0

"""**Length of top-level domains:**"""

def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1

"""**Count digits**"""

def count_digits(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits += 1
    return digits

"""**Count_letters:**"""

def count_letters(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters += 1
    return letters

# Function to extract features from the URL and return them as a pandas DataFrame
def extract_features(url):
    features = []
    features.append(having_ip_address(url))
    features.append(abnormal_url(url))
    features.append(google_index(url))
    features.append(count_dot(url))
    features.append(count_www(url))
    features.append(count_atrate(url))
    features.append(count_dir(url))
    features.append(count_embed_domain(url))
    features.append(suspicious_words(url))
    features.append(short_url(url))
    features.append(count_https(url))
    features.append(count_http(url))
    features.append(count_per(url))
    features.append(count_ques(url))
    features.append(count_hyphen(url))
    features.append(count_equal(url))
    features.append(url_length(url))
    features.append(hostname_length(url))
    features.append(fd_length(url))
    tld = get_tld(url, fail_silently=True)
    features.append(tld_length(tld))
    features.append(count_digits(url))
    features.append(count_letters(url))

    feature_names = ['having_ip_address', 'abnormal_url', 'google_index', 'count_dot', 'count_www', 'count_@',
                     'count_dir', 'count_embed_domain', 'suspicious_words', 'short_url', 'count_https', 'count_http', 'count_%',
                     'count_?', 'count_-', 'count_=', 'url_length', 'hostname_length', 'fd_length',
                     'tld_length', 'count_digits', 'count_letters']

    return pd.DataFrame([features], columns=feature_names)



def XGBoost_Predictions(input_url):

    # Extract features from the input URL
    input_features = extract_features(input_url)

    # Load the XGBoost model from file
    loaded_model = pickle.load(open("URL_Classification/models/XGBoostClassifier.pkl", "rb"))

    # MODELSPATH = 'URL_Classification/models/XGBoostClassifier.pkl'
    # # Load the saved model
    # with open(MODELSPATH, 'rb') as f:
    #     loaded_model = pickle.load(f)

    print(input_features)

    # Make prediction using the loaded model
    output = loaded_model.predict(input_features)
    # print(output)

    return output[0]

# predicted_value = XGBoost_Predictions('https://www.google.com')
# print(predicted_value)