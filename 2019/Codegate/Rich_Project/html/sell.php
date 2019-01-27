<div class="container" style="margin-top:120px">
<?php
	$tax = 50;
	if(!isset($_SESSION['ID']))
		die("login first");
	if($_SESSION['ID'] =="admin")
		die('Fobbiden account');
	sleep(1);
	$conn = dbconn("tradedata");
	$q = "SELECT * FROM user_wallet where id='{$_SESSION['ID']}'";
	$q2 = "SELECT * FROM coin_price order by date DESC limit 1";
	$res = mysqli_query($conn,$q);
	$res2 = mysqli_query($conn,$q2);
	$row = mysqli_fetch_array($res);
	$row2 = mysqli_fetch_array($res2);
	if((int)$_POST['amount'] > $row['coin'] - $tax)
		die("You haven't enough coin (tax : {$tax} coin per 1 trade)");
	$coin = $row['coin'] - ((int)$_POST['amount'] + $tax);
	$cash = $row['cash'] + ((int)$_POST['amount']) * $row2['price'];
	$q = "UPDATE user_wallet SET coin='{$coin}', cash='{$cash}' where id='{$_SESSION['ID']}'";
	mysqli_query($conn,$q);
	mysqli_commit($conn);
	header('Location: ./?p=market');
?>
