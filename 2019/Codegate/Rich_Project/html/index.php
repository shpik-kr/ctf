<?php
	include 'header.php';
	if(isset($_GET['p']))
	{
		switch($_GET['p'])
		{
			case 'pay':
				include 'pay.php';
				break;
			case 'info':
				include '../__SECRET__/pricemaker.php';
				include 'info.php';
				break;
			case 'bbs':
				include '../__SECRET__/pricemaker.php';
				include 'bbs.php';
				break;
			case 'market':
				include '../__SECRET__/pricemaker.php';
				include 'market.php';
				break;
			case 'login':
				include '../__SECRET__/pricemaker.php';
				include 'login.php';
				break;
			case 'reg':
				include '../__SECRET__/pricemaker.php';
				include 'reg.php';
				break;
			case 'write':
				include '../__SECRET__/pricemaker.php';
				include 'write.php';
				break;
			case 'read':
				include '../__SECRET__/pricemaker.php';
				include 'read.php';
				break;
			case 'buy':
				include 'buy.php';
				break;
			case 'sell':
				include 'sell.php';
				break;
			case 'reserv':
				include '../__SECRET__/pricemaker.php';
				include 'reserv.php';
				break;
			case 'logout':
				include '../__SECRET__/pricemaker.php';
				include 'logout.php';
				break;
			default:
				include '../__SECRET__/pricemaker.php';
				include 'home.php';
		}
	}
	else
		include 'home.php';
	include 'footer.php';
?>
