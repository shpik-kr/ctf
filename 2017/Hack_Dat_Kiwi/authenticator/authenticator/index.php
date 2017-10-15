<?php
$url=url();
if (strpos($url,"index.php")!==false)
	$url=dirname($url)."/";
if (isset($_POST['username']))
{
	$username=$_POST['username'];
	$password=$_POST['password'];
	$data="username={$username}|password={$password}";
	if (curl($url."/authenticator.php",["data"=>$data])!=="0")
	{
		echo "Welcome, {$username}! The flag is: ".include __DIR__."/flag.php";
	}
	else
		echo "Invalid username or password.";
}
?>

<p>Please login</p>
<form method='post'>
	<label>Username: </label><input type='text' name='username' /><br/>
	<label>Password: </label><input type='text' name='password' /><br/>
	<input type='submit' />
</form>