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
