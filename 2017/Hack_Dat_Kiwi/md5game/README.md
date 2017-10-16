# [WEB] Hack Dat Kiwi CTF 2017 - md5game1

# Description

>  10 years has passed since MD5 was broken, yet it is still frequently used in web applications, particularly PHP powered applications (maybe because there's a function after it?). Break it again to prove the point!

# Analysis

해당 문제는 `md5($_GET['md5']) == $_GET['md5']`가 성립하는 스트링값을 찾는 문제이다.

이 문제를 풀기전 알아야할 것은 php의 loose comparison이다.

php는 loose comparison과 strict comparison이 존재하며 아래의 링크를 통해 확인할 수 있다.

>  PHP Comparison : http://php.net/manual/en/types.comparisons.php

해당 문제는 loose comparison을 사용하며, 입력 값과 입력 값의 md5값이 완전히 같지 않아도 통과할 수 있다.

>  PHP Magic Hash : https://www.whitehatsec.com/blog/magic-hashes/

즉 0e[0-9]+ 또는 00e[0-9]+와 같은 형태의 스트링으로 md5 해쉬화를 한 값이 0e[0-9]+ 또는 00e[0-9]+와 같은 형태를 하면 된다.

```php
var_dump('0e0'=='0e2'); # true
var_dump('0e0'=='0ea'); # false
var_dump('00e0'=='0e2'); # true
var_dump('00e0'=='00e2'); # true
```

# Exploit

1. PHP Trick using magic hash

## 1. PHP Trick using magic hash

매직 해쉬를 만들기 위해 아래의 간단한 php 스크립트를 돌렸다. 

```php
for($i=0;$i<1000000000;$i++){
  $p= '0e'.intval($i);
  if(md5($p)==$p){
    echo $i;
    break;
  }
}
```

0e215962017의 값이 나왔으며 md5 해쉬 한 값을 0e291242476940776845150308577824이다.

즉 `var_dump('0e215962017' == md5('0e215962017')) = true`가 되어 플래그를 얻을 수 있다.

```html
Wonderbubulous! Flag is zr8cvFTfhd3vcxzH
```



**zr8cvFTfhd3vcxzHzr8cvFTfhd3vcxzH**

