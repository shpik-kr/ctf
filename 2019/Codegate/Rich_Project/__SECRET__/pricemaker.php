<?php
	$PERCENT = 0.50; #if you need, modify this value.

	$conn = dbconn('tradedata');
	$q = "SELECT * FROM coin_price order by Date desc limit 1";
	$res = mysqli_query($conn,$q);
	$row = mysqli_fetch_assoc($res);
	if($row == NULL)
	{
		$q = "INSERT INTO coin_price values(now(),0)";
		mysqli_query($conn,$q);
		mysqli_commit($conn);
		die("");
	}
	$coinPrice = $row['price'];

	$chance = rand()%100/100;
	$value = rand()%50;
	if($PERCENT > $chance)
		$coinPrice += $value;
	else if($coinPrice - $value <=0)
		$coinPrice = $value;
	else
		$coinPrice -= $value;
	$q = "INSERT INTO coin_price values(now(),'{$coinPrice}')";
	mysqli_query($conn,$q);
	mysqli_commit($conn);
?>
