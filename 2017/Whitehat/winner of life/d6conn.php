<?php
	$HOST = "localhost";
	$USER = "lo77o";
	$PASS = "g0db!essU";
	$DB_NAME = "LOTTO";
	$conn = mysqli_connect($HOST,$USER,$PASS,$DB_NAME);

function getRound($conn)
{
	$q = "SELECT max(no)`round` FROM LOG";
	$row = mysqli_fetch_array(mysqli_query($conn,$q));
	if($row['round'] == "")
		$row['round'] = 0;
	return $row['round']+1;
}

?>