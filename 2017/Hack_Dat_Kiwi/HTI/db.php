<?php
function db()
{
	static $db=null;
	if ($db===null)
	{
		$db=new PDO("mysql:host=localhost","root","123456aB");
		$db->exec("use HDK2017;");
		$db->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
		$db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ); 
	}
	return $db;
}
