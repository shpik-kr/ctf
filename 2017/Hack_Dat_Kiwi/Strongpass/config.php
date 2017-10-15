<?
session_start();
if (!is_writable(__DIR__."/history"))
	die("Challenge Error: History folder is not writable.");
if (!is_writable(__DIR__))
	die("Challenge Error: Database folder is not writable.");
if (file_exists(__DIR__."/database.sdb") and !is_writable(__DIR__."/database.sdb"))
	die("Challenge Error: Database is not writable.");
require_once __DIR__."/db.php";
require_once __DIR__."/user.php";

function flag()
{
	var_dump(sql("select * from flag"));
}
