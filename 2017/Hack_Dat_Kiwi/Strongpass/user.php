<?php
function loggedin()
{
	return isset($_SESSION['login']);
}
function signup($username,$password)
{
	if (sql("select * from users where username=?",$username))
		return false;
	return sql("insert into users (username,password) values (?,?)",$username,md5($password));
}
function login($username,$password)
{
	if ($r=sql("select * from users where lower(username)=? and password=?",strtolower($username),md5($password)))
		return $_SESSION['login']=$r[0];
	else
		return false;
}
function logout()
{
	unset($_SESSION['login']);
}
function changepass($oldpass,$newpass)
{
	if (!isset($_SESSION['login'])) return false;
	$userid=$_SESSION['login']['id'];
	if (strlen($newpass)<8) return false;
	if (!sql("select * from users where id=? and password=?",$userid,md5($oldpass)))
		return false;
	if ($newpass===$oldpass) return false;
	function get_password_history()
	{
		$file=password_history_file();
		if (!file_exists($file))
			return [];
		else
			return explode(PHP_EOL,file_get_contents($file)); 
	}
	function password_history_file()
	{
		$username=$_SESSION['login']['username'];
		return realpath(__DIR__."/history")."/".substr("{$username}.pss",0,255);//filename length limit
	}
	//check if password not used before
	$hash=hex2bin(md5($newpass));
	$pass_history=get_password_history();
	foreach ($pass_history as $one_of_old_passes)
		if ($hash===$one_of_old_passes)
			return false;
	array_unshift($pass_history, $hash);
	file_put_contents(password_history_file(), implode(PHP_EOL,$pass_history));
	return sql("update users set password=? where id=?",md5($newpass),$userid);
}