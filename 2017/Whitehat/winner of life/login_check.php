<?php
	session_start();
	include 'd6conn.php';

	if($_SESSION['id'])
		die("<script> alert('already login!'); location.href='./';</script>");
	$id = addslashes($_POST['userid']);
	$pw = addslashes($_POST['userpw']);

	$q = "SELECT * FROM ACCOUNT WHERE id='{$id}' and pw=md5('{$pw}')";
	$row = mysqli_fetch_array(mysqli_query($conn,$q));
	if($row['id'])
	{
		if($row['IP'] != $_SERVER['REMOTE_ADDR'])
			die("<script>alert('Different IP is detected.'); history.go(-1);</script>");

		$_SESSION['id'] = $id;
		die("<script> alert('Welcome!'); location.href='./';</script>");
	}
	else
		die("<script> alert('Check your account info.'); history.go(-1);</script>");	
?>