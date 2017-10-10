# [Crypto] Kaspersky 2017 - decrypt the message

# Description
Could your decrypt the message? http://95.85.51.183

# Analysis
페이지에 접속하면 `missing parameter: name`란 문구가 나온다.

파라미터로 name=1을 넘겨주면 `Hello 1`으로 변경되며, 이때 cookie값을 생성해준다.
```
user_info=laohzfIjJ0KMBkuTU4VUph5LAW6n9I5siXZeqC42febijJUkD3+VUtcLq0nVr/tVBjmQgppbinbAnz2H5zgl5A==
```

여기서 맨 끝 A\=\=을 Q\=\=로 변경하여 서버에 요청하면 다음과 같은 에러가 발생한다.
```
Traceback (most recent call last):
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1612, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1598, in dispatch_request
return self.view_functions[rule.endpoint](**req.view_args)
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 53, in index
user_info_decrypted = json.loads(aes_decrypt(user_info).decode())
File "/usr/lib/python2.7/json/__init__.py", line 339, in loads
return _default_decoder.decode(s)
File "/usr/lib/python2.7/json/decoder.py", line 364, in decode
obj, end = self.raw_decode(s, idx=_w(s, 0).end())
File "/usr/lib/python2.7/json/decoder.py", line 382, in raw_decode
raise ValueError("No JSON object could be decoded")
ValueError: No JSON object could be decoded
```

오 AES로 암호화 한다.

또다른 에러를 보자.
```
Traceback (most recent call last):
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1612, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1598, in dispatch_request
return self.view_functions[rule.endpoint](**req.view_args)
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 53, in index
user_info_decrypted = json.loads(aes_decrypt(user_info).decode())
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 34, in aes_decrypt
cipher = AES.new(base64.b64decode(hardcoded_key), AES.MODE_CBC, iv )
File "/usr/local/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 95, in new
return AESCipher(key, *args, **kwargs)
File "/usr/local/lib/python2.7/dist-packages/Crypto/Cipher/AES.py", line 59, in __init__
blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
File "/usr/local/lib/python2.7/dist-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
self._cipher = factory.new(key, *args, **kwargs)
ValueError: IV must be 16 bytes long
```
오 블록사이즈가 16바이트인 AES-CBC이다.

Oracle Padding 각이 나온다.

# Exploit
1. Oracle Padding

## 1. Oracle Padding
오라클 패딩이라 함은 디코드 성공과 실패(또는 서버 반응)을 기준으로 공격을 하는데, 해당 문제는 **항상** 500 Error와 함께 다양한 에러문을 뿌려준다.(에러문의 종류는 5가지 이상이다.)

많은 에러문 중 아래의 에러 유형을 통해 평문을 추출할 수 있을 것 같다.
```
Traceback (most recent call last):
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1612, in full_dispatch_request
rv = self.dispatch_request()
File "/usr/local/lib/python2.7/dist-packages/flask/app.py", line 1598, in dispatch_request
return self.view_functions[rule.endpoint](**req.view_args)
File "/var/www/FlaskApp/FlaskApp/__init__.py", line 53, in index
user_info_decrypted = json.loads(aes_decrypt(user_info).decode())
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 16: ordinal not in range(128)
```
16번째 위치에서 0xe9를 ascii로 디코드 못하는 에러이다.

그래서, 이번 문제는 기존 Oracle Padding과는 다르게 해당 에러를 통해 문자열을 추출하기로 하였다.

Oracle Padding에서는 평문을 `(intermediary) ^ (조작된 IV) ^ (조작된 평문)`의 연산을 통해 얻는다.
> intermediary ^ iv = 평문
> 
> 조작된 평문 ^ 조작된 iv = intermediary
> 
> 조작된 평문 ^ 조작된 iv ^ intermediary = 평문
> 

```python
import urllib
import urllib2

e_b64 = lambda x:x.encode('base64').replace('\n','')
d_b64 = lambda x:x.decode('base64')

url = 'http://95.85.51.183/'
ciphertext = d_b64('laohzfIjJ0KMBkuTU4VUph5LAW6n9I5siXZeqC42febijJUkD3+VUtcLq0nVr/tVBjmQgppbinbAnz2H5zgl5A==')
bs = 16
plain = ''
def r(cookie, idx):
    global url
    try:
        req = urllib2.Request(url)
        req.add_header('Cookie','user_info= %s'%(e_b64(cookie)))
        res = urllib2.urlopen(req)
        data = res.read()
    except urllib2.HTTPError, e:
        if e.getcode() == 500:
            data = e.read()
            if 'UnicodeDecodeError: \'ascii\'' in data:
                tmp = data.split('codec can\'t decode byte ')[1]
                d = tmp.split(' in')[0][2:]
                p = int(tmp.split('position ')[1].split(':')[0])
                if idx == p:
                    return int(d,16)
                return -1

for i in range(len(ciphertext)/bs):
    cipher = ciphertext[i*bs:]
    for idx in range(0x00,0x10):
        for k in range(0x00,0x100):
            mal_cipher = cipher[:idx] + chr(k) + cipher[idx+1:]
            d = r(mal_cipher, idx)
            if d > -1:
                plain += chr(d^ord(cipher[idx])^k)
                print '[+] %d(%s): %s '%(idx,(chr(d^ord(cipher[idx])^k)),plain)
                break
            else:
                continue
```
위 스크립트를 통해 평문 `{"name": "1", "show_flag": false}`를 얻었다.

이제 이를 `{"name": "1", "show_flag": true }`로 변조하기 위한 스크립트를 작성하였다.
> 평문 ^ IV ^ 조작된 평문 = 조작된 IV
> 

```python
import urllib
import urllib2

e_b64 = lambda x:x.encode('base64').replace('\n','')
d_b64 = lambda x:x.decode('base64')

url = 'http://95.85.51.183/'
ciphertext = d_b64('laohzfIjJ0KMBkuTU4VUph5LAW6n9I5siXZeqC42febijJUkD3+VUtcLq0nVr/tVBjmQgppbinbAnz2H5zgl5A==')
plaintext = '{"name": "1", "show_flag": false}'
mal_plain = '{"name": "1", "show_flag": true }'
bs = 16

def r(cookie, idx):
    global url
    try:
        req = urllib2.Request(url)
        req.add_header('Cookie','user_info= %s'%(e_b64(cookie)))
        res = urllib2.urlopen(req)
        data = res.read()
    except urllib2.HTTPError, e:
        if e.getcode() == 500:
            data = e.read()
            if 'UnicodeDecodeError: \'ascii\'' in data:
                tmp = data.split('codec can\'t decode byte ')[1]
                d = tmp.split(' in')[0][2:]
                p = int(tmp.split('position ')[1].split(':')[0])
                if idx == p:
                    return int(d,16)
                return -1

# plain ^ malformed_plain ^ iv = malformed_iv [ block 1 ]
mal_tmp = ''
for j in range(16):
    mal_tmp += chr(ord(plaintext[bs+j])^ord(mal_plain[bs+j])^ord(ciphertext[bs+j]))

cipher = ciphertext[:16]+mal_tmp+ciphertext[32:]

# [ block 0 : IV ]
cookie = ''
for idx in range(0x00,0x10):
    for k in range(0x00,0x100):
        mal_cipher = cookie + chr(k) + cipher[idx+1:]
        d = r(mal_cipher, idx)
        if d > -1:
            cookie += chr(d^k^ord(plaintext[idx]))
            print '[+] %d(%s): %s '%(idx,(chr(d^k^ord(plaintext[idx])).encode('hex')),cookie)
            break
        else:
            continue

cookie += cipher[16:]

print '[*] Cookie : %s'%(cookie)
print '[*] Cookie base64 : %s'%(e_b64(cookie))
```

해당 스크립트를 실행하면 show_flag의 값을 true로 변조한 AES암호문인 `9IFW+NxuSSzUPgdiYnJd2h5LAW6n9I5siXZeuj0va6PijJUkD3+VUtcLq0nVr/tVBjmQgppbinbAnz2H5zgl5A==` 나오고, 이를 cookie의 user_info에 덮어씌우면 플래그를 얻을 수 있다.
```html
Hello 1<br>Flag: KLCTFFDA616A6DAF4E63A9F7B55B43124E548<br>
```

**KLCTFFDA616A6DAF4E63A9F7B55B43124E548**
