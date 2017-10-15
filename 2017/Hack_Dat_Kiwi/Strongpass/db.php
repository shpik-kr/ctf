<?php

function db_setup()
{
	sql("create table if not exists users (id integer primary key autoincrement, username text, password text)");
}
function db()
{
	static $db=null;
	if ($db===null)
	{
		$db=new PDO("sqlite:".__DIR__."/database.sdb");
		db_setup();
	}
	return $db;
}
function sql()
{
	$args=func_get_args();
	$query=array_shift($args);
	$s=db()->prepare($query);
	if (!$s) die(var_export(db()->errorInfo()));
	$s->execute($args);
	$type=strtolower(substr(trim($query),0,6));
	if ($type==="select")
		return $s->fetchAll();
	elseif (in_array($type,['create','update','insert','replac']))
		return $s->rowCount();
	else
		return $s;
}