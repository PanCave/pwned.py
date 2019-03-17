import hashlib
import pycurl as curl
from io import BytesIO
import certifi as cert
import sys

url = 'https://api.pwnedpasswords.com/range/'
useragent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;en; rv:5.0) Gecko/20110619 Firefox/5.0'

if len(sys.argv) == 2:
    print('Checking Password: ', sys.argv[1])
    hash = hashlib.sha1(sys.argv[1].encode())
    hash_str = hash.hexdigest()
    hash_str_first = hash_str[:5]
    hash_str_last = hash_str[5:]
    buffer = BytesIO()
    c = curl.Curl()
    c.setopt(curl.USERAGENT, useragent)
    c.setopt(c.CAINFO, cert.where())
    c.setopt(c.URL, url+hash_str_first)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    hashes_found = body.decode('iso-8859-1').splitlines(False)
    has_found = False
    for h in hashes_found:
        if h.split(':')[0].lower() == hash_str_last:
            print('Found Password in ' + h.split(':')[1] + ' lists. Consider not using it!')
            has_found = True
            break
    if not has_found: print('Password has not been leaked yet')
