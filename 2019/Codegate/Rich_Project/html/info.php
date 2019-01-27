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
