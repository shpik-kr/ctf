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
