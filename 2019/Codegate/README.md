# Codegate 2019 Quals

최악의 대회여서 딱히 할말이 없다. ~~(허스트게이트)~~

## Solved Problem

- Rich Project - Web/SQLi/Fxck
- PyProt3ct - Rev/Python/VM/Crackme
- mini converter - Pwn/Ruby/1-day/Overflow

## writeup

### Rich Project

거래소 느낌을 내고싶어 하는 페이지가 보입니다만, 그냥 랜덤하게 뿌려주는 것 같습니다.

robots.txt통해 Source code가 들어가 있는 압축파일을 얻을 수 있는데, 압축 해제를 의해서는 **패스워드**가 필요합니다.

그리고 게시판에는 admin만 읽을 수 있는 notice가 존재하는데, 이를 읽어야 압축을 풀 수 있을거 같은 느낌입니다.

info 메뉴로 가면 돈이 9999999? 이상일 때, 무언가를 얻을 수 있습니다.

그러면 우선 admin계정을 얻거나, XSS를 이용해 페이지를 읽어야 하므로 취약점을 찾으러 갔습니다.

회원 가입 시, **SQL Injection**이 발생합니다.

몇몇의 문자열에 대해 **필터링**이 되어 있습니다.

```
where, limit, group_concat, board, ...
```

위이 필터링에 걸리지 않게 쿼리를 만들어서 admin의 패스워드, AC를 획득해줍니다.

**Query :** '+ord(mid((select x from (select id,ac x from users a having id=0x61646d696e)x),1,1)))-- -

이를 통해 로그인하여 notice를 읽으면 **MASTER\_PW**를 얻을 수 있습니다.

**MASTER_PW** : D0\_N0T\_RE1E@5E\_0THER5

info 페이지의 소스코드를 볼 수 있습니다.

```
<!-- info.php -->
<?php 
	if(!isset($_SESSION['ID']))
		die('<div class="container" style="margin-top:120px">login first');
	$conn = dbconn('tradedata');
	$conn2 = dbconn('userdata');
	$q = "SELECT * FROM user_wallet where id='{$_SESSION['ID']}'";
	$q2 = "SELECT * FROM users where id='{$_SESSION['ID']}'";
	$res = mysqli_query($conn,$q);
	$res2 = mysqli_query($conn2,$q2);
	$row = mysqli_fetch_array($res);
	$row2 = mysqli_fetch_array($res2);
?>
    <div class="container marketing" style="margin-top: 120px;">
    <b>Check your data:<br></b>
	ID : <?php echo $row['id'];?><br>
	PW : ****<br>
	AC : <?php echo $row2['ac'];?><br>
	GOLD : <?php echo $row['cash']?><br><br>

	<b>if you want more gold, please deposit money in this account.</b><br>
	<u>7777-777777-7777, SCAM bank</u><br><br>

	<b>if you give to 999999999 money, I will give to you "GOOD THINGS"</b>
	<br>
	<a href="./?p=pay"><button type="button" class="btn btn-primary">Buy good things</button></a>
	
<!-- pay.php -->
<div class="container" style="margin-top:120px">
<?php
	if(!isset($_SESSION['ID']))
		die('login first');
	$conn = dbconn('tradedata');
	$q = "SELECT * FROM user_wallet where id='{$_SESSION['ID']}'";
	$res = mysqli_query($conn,$q);
	$row = mysqli_fetch_array($res);
	if($row['cash'] <999999999)
		die("Not enough gold");
	else
		include '../__SECRET__/flag.php';
?>

<!-- ../__SECRET__/flag.php -->
<?php
	$key= "D0_N0T_RE1E@5E_0THER5";
	$FLAG = "##########"
	if($_GET['key'] === $key)
		die($FLAG);
	else
		die("who you are?");
?>
```

Source Code를 보면 돈이 999999999이상일 때, flag를 줍니다.

*돈을 벌러 가야합니다.* (아니..)

코인(?) 거래를 할 때, 일반 구매, 판매 말고 Reserv라는 기능이 하나 더 있습니다.

이는 **MASTER_PW**를 알아야지만 이용할 수 있는 기능입니다.

```
<div class="container" style="margin-top:120px">
<?php
	$MASTER_PW = "D0_N0T_RE1E@5E_0THER5"; #Already you know this, right?
	if(!isset($_SESSION['ID']))
		die("login first");
	if($_SESSION['ID'] =="admin")
		die('Fobbiden account');

	$time = strtotime($_POST['date']);
	if($time === NULL || $time < 0)
		die("detect input error");
	if($time < time() || $time > time()+60*60*24*365*20)
		die("detect input error");
	$count = addslashes($_POST['amount']);
	if($_POST['code'] !== $MASTER_PW)
		die("Input reserv password");

	$conn = dbconn('tradedata');
	$q = "SELECT * FROM user_wallet where id = '{$_SESSION['ID']}'";
	$res = mysqli_query($conn,$q);
	$row = mysqli_fetch_assoc($res);

	$q = "UPDATE user_wallet SET reserv=from_unixtime({$time}),amount='{$count}' where id='{$_SESSION['ID']}'";
	mysqli_query($conn,$q);
	mysqli_commit($conn);
	header('Location: ./?p=market');

?>
```

Source Code에 따라 POST형식에 맞춰서 날려주니 돈이 200억이 되었습니다.

그 돈으로 플래그를 구매할 수있습니다.

**FLAG :** H0LD_Y0UR_C0IN_T0_9999-O9-O9!



### PyProt3ct

Python으로 구현된 VM 문제입니다.

VM문제 특성상 Disassembler를 만들어주면 됩니다. [[Link]()]

분석을 해보면 패스워드는 8자리이며, 특정 연산을 마쳤을 시 일정한 값이 나와야 합니다.

VM으로 처리하는 연산을 파이썬으로 구현한 코드는 다음과 같습니다.

```python
checked = (((((((((flag[0]+0)<<8 + flag[1])<<8 + flag[2])<<8 + flag[3])<<8) + flag[4] << 8 + flag[5])<<8) <<8 + flag[6])<<8) + flag[7]

for i in range(127):
	a1 = (((checked & 0xFFFFFFFF) ^ 4290952684) + 4290952684 ) & 0xFFFFFFFF
	a2 = (((checked >> 32)^4290952684) + 4290952684 ) & 0xFFFFFFFF
	a1 = a1 << 32
	t1 = a1|a2
	t1_tmp = t1 >> 7
	t2_tmp = (t1 << 57)&0xFFFFFFFFFFFFFFFF
	t1 = t1_tmp | t2_tmp
	checked = t1 & 18446744073709551615

if checked == 15164928151071436234:
	return 1
return 0
```

이를 역연산하면 간단하게 플래그를 얻을 수 있습니다.

```python
checked = 15164928151071436234
res = 0

for i in range(127):
	if checked + 18446744073709551615 > 0xFFFFFFFFFFFFFFFF:
		checked = checked
	else:
		checked += 18446744073709551615
	bb = (checked << 7)
	aa = ((checked >> 57))&0x7F
	tmp_a = (bb | aa)&(0xFFFFFFFFFFFFFFFF)
	bb = tmp_a >> 32
	a1 = ((((bb - 4290952684)&0xFFFFFFFF)^4290952684))&0xFFFFFFFF

	a2 = (((((tmp_a))-4290952684)&0xFFFFFFFF)^4290952684) << 32

	checked = (a1 | a2)&0xFFFFFFFFFFFFFFFF

print `hex(checked)[2:-1].decode('hex')`
'''
`d34dPY27`
'''
```

**FLAG** : d34dPY27