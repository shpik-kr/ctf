<?php
	include 'header.php';
	switch($_GET['p'])
	{
		case "login":
			include 'login.php';
			break;
		case "reg":
			include 'register.php';
			break;
		case "buy":
			include 'buy.php';
			break;
		case "logout":
			include "logout.php";
			break;
		case "result":
			include "result.php";
			break;
		case "history":
			include "history.php";
			break;
		case "statistics":
			include "statistics.php";
			break;
		case "DEEEBUG":
			phpinfo();
		default:
			include 'main.php';
			break;
	}
	
?>