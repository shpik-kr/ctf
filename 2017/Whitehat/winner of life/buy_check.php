<?php
	session_start();
	include 'd6conn.php';
	if(!$_SESSION['id'])
		die('<script> alert("LOGIN FIRST"); location.href="./?p=login"; </script>');
	### CHECK VALID VALUE ###
	if(sizeof($_POST) != 7)
		die("<script> alert('You MUST check exactly 7 numbers.'); history.go(-1);</script>");
	foreach( $_POST as $k => $v )
	{
		if($k != $v)
			die("<script> alert('Input error.. Intersting..'); history.go(-1);</script>");
		if(!is_numeric($k))
			die("<script> alert('DO NOT MODIFY NUMBERS TO STRING'); history.go(-1);</script>");
	}

	### INSERT TO DATABASE ###
	$Data = implode(",",$_POST);
	$Round = getRound($conn);
	$time = date("Y-m-d H:i:s");
	$q = "INSERT INTO ATTEMPT value('{$Round}','{$_SESSION['id']}','{$Data}','{$_SERVER['REMOTE_ADDR']}','{$time}')";
	$res = mysqli_query($conn,$q);
	if( mysqli_errno($conn) == 1062 )
		die("<script> alert('You already attempt this round. Please wait.'); location.href='./';</script>");
	else
		die("<script> alert('Your luckyNumber is ".$Data.". Good luck!'); location.href='./';</script>");
?>