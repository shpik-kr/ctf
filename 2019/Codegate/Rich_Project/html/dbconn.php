<?php
	function dbconn($dbname)
	{
		$HOST = ""; #File Cracked :p
		$USER = ""; #File Cracked :p
		$PASS = ""; #File Cracked :p
		$ret = mysqli_connect($HOST,$USER,$PASS,$dbname);
		return $ret;
	}
?>
