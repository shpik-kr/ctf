<?php
	session_start();
	include 'd6conn.php';
	$id = addslashes($_POST['userid']);
	$pw = addslashes($_POST['userpw']);
	$q = "INSERT INTO ACCOUNT VALUES('{$id}',md5('{$pw}'),'{$_SERVER['REMOTE_ADDR']}')";
	mysqli_query($conn,$q);
	if(mysqli_errno($conn) == 1062)
		die( "<script> alert('ID DULPLICATED.'); history.back()</script>");
	else if (mysqli_errno($conn) == 0)
	{
		$_SESSION['id'] = $id;
		die( "<script> alert('OK. Enjoy your lotto'); location.href='./';</script>" );
	}
	else
		die("Unknown error occur");
	
?>