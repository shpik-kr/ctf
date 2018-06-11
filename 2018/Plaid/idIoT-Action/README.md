# [Web] Plaid CTF - idIoT: Action

## Description

Some people won't let any smart devices in their home at all. Some are cautious, do their research, and make an informed decision. This guy falls in neither category; he's a a downright idIoT.

The idIoT uses this service called [clipshare](https://idiot.chal.pwning.xxx/); you can find his account [here](https://idiot.chal.pwning.xxx/user.php?id=3427e48e-a6eb-4323-aed4-3ce4a83d4f46) or [here](https://idiot.chal.pwning.xxx/user.php?id=8660d251-d77c-4316-ac2c-a9a0662e6240) after you make an account.

He was telling me the other day about how he has a Google Home next to his computer running at all times. He also told me that if you ask politely it will tell you the flag. However, while he'll look at anything you share, he closes it almost immediately if he doesn't seem like it'll interest him. Maybe we can look at his clips to find something to match his interests?

(Flag format: PCTF{xxx} where xxx is some text composed of lower-case letters and underscores)

## Analysis

문제에 들어가면 다음과 같이 로그인 페이지가 나타나며, Register 후 로그인할 수 있다.

![idiot_main_page](pctf2018-dliot-01.png)

로그인 하면 아래와 같은 페이지가 나타나며 사용할 수 있는 메뉴는 Create a clip, shares, shpikgod, logout이다.

![idiot_main_page_after_login](pctf2018-dliot-02.png)

메뉴에 대해 간단히 설명하면 다음과 같다.

- CREATE A CLIP : 새로운 클립을 생성한다.
- SHARES : 공유받은 클립을 보여준다.
- SHPIKGOD : Profile 페이지으로 로그인 시 처음 나타는 화면이며, 자신이 작성한 클립을 보여준다.(위의 이미지 사진)
- LOG OUT : 로그아웃

CREATE A CLIP을 통해 XSS을 유발하는 스크립트를 삽입하여 관리자 계정(idiot1)로 SHARE를 하면 Bot이 이를 읽어 세션을 탈취하는 문제인 것 같다.

우선 헤더를 살펴보면 CSP가 걸려있는 것을 확인할 수 있다.

```
Cache-Control: no-store, no-cache, must-revalidate
Connection: Keep-Alive
Content-Encoding: gzip
Content-Length: 408
Content-Security-Policy: style-src 'self' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; media-src 'self' blob:; script-src 'self'; object-src 'self'; frame-src 'self'
Content-Type: text/html; charset=UTF-8
Date: Wed, 09 May 2018 15:33:55 GMT
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Keep-Alive: timeout=5, max=100
Pragma: no-cache
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept-Encoding
```

어마무시한 CSP가 걸려있는데 img 태그는 self가 안걸려있으므로, 이를 이용해 bot이 돌고있는지 확인하였다.

```html
<img src="[SERVER]">
```

봇은 돌고있는 것을 확인하였으니, 스크립트를 삽입하여 쿠키를 획득해야한다.

하지만 CSP  `script-src 'self'`에 의해 외부의 스크립트는 로드할 수 없으며, 또한 unsafe-inline에 의해 스크립트 삽입이 불가능하다.

그 다음의 풀이는 다음과 같다.

wave 파일은 script 로드 시 javascript로써 로드할 수 있다.

이를 이용하면 플래그를 얻을 수 있다. 



- 대회 끝나고 문제의 봇이 작동을 안해.... 더이상 진행이 불가능하였습니다.

