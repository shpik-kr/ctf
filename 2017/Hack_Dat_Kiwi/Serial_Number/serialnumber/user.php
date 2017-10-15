<?php
function isadmin($user)
{
	return sql("select ? in (select serialnumber from serialnumbers) as result",$user->serialnumber)[0]->result!=="0";
}
function loggedin()
{
	return isset($_SESSION['login']);
}
function user()
{
	if (loggedin())
		return $_SESSION['login'];
	else
		return null;
}
function signup($username,$password,$serialnumber)
{
	if (!ctype_alnum($serialnumber)) return false;
	if (!ctype_alnum($username)) return false;
	if (!$username or !$serialnumber) return;
	if (sql("select * from users where username=?",$username))
		return false;
	return sql("insert into users (username,password,serialnumber) values ('$username','".md5($password)."',{$serialnumber})");
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
