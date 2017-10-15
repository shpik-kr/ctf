<?php
require_once "config.php";
if (isset($_GET['password']))
{
	$res=select("*", "secrets","password='{$_GET['password']}'");
	if ($res and $obj=$res[0])
		echo "flag as answer"," ( {$obj->flag} )",PHP_EOL;
	else
		echo "Invalid password.";
}

?>

Do you have the password? Enter it below.

<form method='get'>
	Password: <input type='text' name='password' /><input type='submit' />
</form>


<a href='ticket.php'>Contact Us</a>


