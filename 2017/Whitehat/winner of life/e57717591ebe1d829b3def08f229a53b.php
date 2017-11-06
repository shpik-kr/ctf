#!/usr/bin/php
<?php
	include '9en3rat0r.php';
	include 'd6conn.php';
	//if(time()>1509576900)
	//{
		### MAKE LOTTO NUMBERS ###
		$luckyNumber = generator();
		sort($luckyNumber);
		$luckyNumber = implode(",",$luckyNumber);

		### CHECK ROUND ###
		$round = getRound($conn);

		### CHECK WINNER ###
		$q = "SELECT * FROM ATTEMPT WHERE no={$round}";
		$res =mysqli_query($conn,$q);
		$Winners = array();
		while($row = mysqli_fetch_array($res))
		{
			if($luckyNumber == $row['numbers'])
				array_push($Winners,$row['name']);
		}

		### WRITE HISTORY ###
		$Winners = implode(",",$Winners);
		$q = "INSERT INTO LOG(luckyNumbers,winners) values('{$luckyNumber}','{$Winners}')";
		$res = mysqli_query($conn,$q);

		### WRITE CURRENT TIME ###
		$f = fopen("/var/www/T1M3","w");
		fwrite($f,date("Y-m-d H:i:s"));
		fclose($f);
	//}
?>