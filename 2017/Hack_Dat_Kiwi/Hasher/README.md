# [WEB] Hack Dat Kiwi CTF 2017 - Hasher

# Description

>   There's this system that has a hardcoded admin user/password, in a way that can not be brute forced or cracked. We desperately need to acquire access to this system, can you help us?

# Analysis

문제 페이지에 접속하면 소스코드를 보여준다.

```php
<?php
if (!shell_exec("which openssl"))
    die("Challenge Error: need openssl installed\n");
if (isset($_GET['code']))
    die(highlight_file(__FILE__));
function str_xor($str,$max_depth=0,$depth=0)
{
    $mid=strlen($str)/2;
    $left=substr($str,0,$mid);
    $right=substr($str,$mid);
    if ($depth<$max_depth)
    {
        $left=str_xor($left,$max_depth,$depth+1);
        $right=str_xor($right,$max_depth,$depth+1);
    }
    $out="";
    for ($i=0;$i<strlen($left);++$i)
        $out.=$left[$i]^$right[$i];
    return $out;
}
function hasher($string)
{
    if (!ctype_alnum($string))
        return null;
    $t=trim(shell_exec("echo -n '{$string}' | openssl dgst -whirlpool | openssl dgst -rmd160"));
    $t=str_replace("(stdin)= ","",$t); //some linux adds this
    if (!$t)
        return null;
    return bin2hex(str_xor(hex2bin($t),1));
}
$user='admin';
extract($_POST);
if (isset($password))
{
    if (hasher($user)==hasher($password) and $user!=$password)
        echo "Welcome! Flag is: ".include("flag.php");
    else
        echo "Invalid password.<br/>";
}
?>
<form method='post'>
    <label>Password:</label>
    <input type='password' name='password' />
    <input type='submit' />
</form>
<a href='./?code'>Source Code</a>
```

user과 password 값이 같지 않으면서 hasher 함수의 리턴값이 같아야 flag를 얻을 수 있다.

hasher 함수를 보면 제일 먼저 ctype_alnum함수로 입력 값이 알파벳+숫자인지 체크해주고, 그 후 shell_exec를 통해 암호화 한다.

마지막으로 str_xor함수를 통해 xor연산을 해준다.

# Exploit

처음에는 shell_exec를 이용한 커맨드 인젝션인 줄 알았는데, 자세히 보니 아니였다.

위 소스에서 내가 공격한 부분은 다음과 같다.

```php
function hasher($string)
{
    if (!ctype_alnum($string))
        return null;
# 중략
}
```

hasher함수 첫 부분에서 ctype_alnum이 아니면 null값을 리턴해준다.

또한 해당 페이지에는 `extract($_POST);`를 사용해 POST값을 풀어주는데 extract함수에는 취약점이 존재한다.

>  extract() 함수는 이전에 정의된 변수의 값을 변경할 수 있다.

이를 이용하여 $user의 값을 @로 변경하고 $password의 값을 \*로 하여 POST로 넘겨주면 hasher 함수에서 ctype_alnum 함수에 의해 null이 리턴되고, 최종적으로 `if (hasher($user)==hasher($password) and $user!=$password)`의 식이 `if(null==null and '@'!='*')`이 되어 flag를 얻을 수 있다.

```html
Welcome! Flag is: g1diXbB2kfaGjS0V.
```



**g1diXbB2kfaGjS0V**