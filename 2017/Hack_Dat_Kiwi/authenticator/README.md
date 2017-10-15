# [WEB] Hack Dat Kiwi CTF 2017 - Authenticator

# Description

>   문제 페이지 닫힘

# Analysis

해당 문제는 소스파일을 제공해준다.

소스는 다음과 같다.

```php+HTML
<!-- index.php -->
<?php
$url=url();
if (strpos($url,"index.php")!==false)
	$url=dirname($url)."/";
if (isset($_POST['username']))
{
	$username=$_POST['username'];
	$password=$_POST['password'];
	$data="username={$username}|password={$password}";
	if (curl($url."/authenticator.php",["data"=>$data])!=="0")
	{
		echo "Welcome, {$username}! The flag is: ".include __DIR__."/flag.php";
	}
	else
		echo "Invalid username or password.";
}
?>

<p>Please login</p>
<form method='post'>
	<label>Username: </label><input type='text' name='username' /><br/>
	<label>Password: </label><input type='text' name='password' /><br/>
	<input type='submit' />
</form>
```

```php+HTML
<!-- config.php -->
<?php
// ini_set("display_errors",false);
assert(ini_get("max_input_vars")<=1000);
assert(ini_get("max_input_time")=="-1" or ini_get("max_input_time")>=30);
ini_set("max_execution_time","2");
set_time_limit(2);
assert(ini_get("post_max_size")<=2); 
ini_set("memory_limit",(ini_get("post_max_size")*32)."M");

function curl($url,$postparams=[])
{
	$opts=[
		CURLOPT_COOKIEJAR => 'kiwimaster.cookie',
		CURLOPT_COOKIEFILE => 'kiwimaster.cookie',
    	CURLOPT_RETURNTRANSFER => 1,
    	CURLOPT_URL => $url,
    	CURLOPT_USERAGENT => 'Kiwi Master'
	];
	if ($postparams)
	{
		$opts[CURLOPT_POST]=1;
		$opts[CURLOPT_POSTFIELDS]=http_build_query($postparams);
	}
	$curl = curl_init();
	curl_setopt_array($curl, $opts);
	$res = curl_exec($curl);
	curl_close($curl);
	return $res;
}
function url()
{
	return "http://localhost/$_SERVER[REQUEST_URI]";
	return "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

}
```

```php+HTML
<!-- authenticator.php -->
<?php
//"username={$username}|password={$password}";
@$data=$_POST['data'];


$r=explode("|",$data);
$arr=[];
if ($r)
foreach ($r as $t)
{
	if (strpos($t,"=")===false) continue;
	$arr[explode("=",$t)[0]]=explode("=",$t)[1];
}
if (!isset($arr['username']) or !isset($arr['password']))
	die('0');
if (md5($arr['username'].$arr['password'])!=="b4dae82ae3c7484f725a667e5ecc4e78")
	die("0");

die("1");
```

```shell
# .htaccess
php_value include_path .:..:../..
php_value short_open_tag on
php_value max_execution_time 1
php_value max_input_time -1
php_value max_input_vars 1000
php_value post_max_size 2M
php_value upload_max_filesize 2M
php_value auto_prepend_file config.php
Order Deny,Allow
Deny from all

<FilesMatch ^$|\.php$|\.js$|\.css$>
        Allow from all
</FilesMatch>
```

소스들을 보면 index.php에서 `if (curl($url."/authenticator.php",["data"=>$data])!=="0")`의 조건문이 성립하면 flag를 주는 문제이다.

우선 index.php의 첫번째 라인에서 `$url=url();`에 의해 curl을 수행할 url이 리턴된다.(해당 url은 `http://localhost/$_SERVER[REQUEST_URI]`로써 SSRF는 불가능해 보인다.)

curl함수는 config.php에서 정의되었으며, 기존의 알고있는 리눅스 명령어 curl과 같은 역할을 한다.

즉 curl을 통해 `authenticator.php`페이지에 우리가 입력한 username과 password를 기반으로 0또는 1을 리턴해주고, 이를 기반으로 위의 `if (curl($url."/authenticator.php",["data"=>$data])!=="0")`의 참 거짓이 정해진다.

# Exploit

1. Filtering bypass

## 1. Filtering bypass

해당 공격은 ***제작자의 의도에 맞지 않은 풀이법***으로써 대회 중 점수가 깍였다. ~~(문제를 제대로좀 내지..)~~



index.php 소스의 일부분을 보자.

```php
$url=url();
if (strpos($url,"index.php")!==false)
	$url=dirname($url)."/";
# 중략
if (curl($url."/authenticator.php",["data"=>$data])!=="0")
	{
		echo "Welcome, {$username}! The flag is: ".include __DIR__."/flag.php";
	}
```

config.php에 정의된 url 함수를 통해 리턴받는 값은  `http://localhost/$_SERVER[REQUEST_URI]`이다.

>  요청한 페이지가 http://g64.shpik.xyz/this/is/test.php?me=too#hi 일 경우  $_SERVER['REQUEST_URI']의 값은 `this/is/test.php?me=too`가 된다.

이를 이용하여 url을 `http://7a0567.2017.hack.dat.kiwi/web/authenticator/?`를 요청하고 아이디 패스워드를 아무 거나 입력 한 후 전송한다.

그러면 curl에 의해 요청된는 페이지는 `http://localhost/web/authenticator/?authenticator.php` 가 되고, 요청되는 페이지는 결국 index.php가 되어 0이 아닌 값이 리턴되어 조건문이 참이 되어 flag를 얻을 수 있다.

```html
Welcome, asd! The flag is: 29874hyfewqjadijv
```



**29874hyfewqjadijv**









