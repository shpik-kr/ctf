<?php
function db_setup()
{
	sql("CREATE TABLE IF NOT EXISTS `serialnumbers` (
  `serialnumber` int(11) primary key
);

INSERT INTO `serialnumbers` (`serialnumber`) VALUES
(0xdeadbeef),
(287364618);

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) primary key auto_increment,
  `username` varchar(64) ,
  `serialnumber` int(11) ,
  `password` varchar(128)
);

INSERT INTO `users` (`username`,`serialnumber`,`password`) VALUES 
('admin',0xdeadbeef,'8a26855bd1fe07fc3ec200dfa95cbc55'),
('kiwimaster',287364618,'b91f928fb04ab6ce909d46280a00133b');

CREATE TABLE IF NOT EXISTS `flag` (
  `flag` varchar(64)
);
ALTER TABLE `users`
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `serialnumber` (`serialnumber`),
  ADD UNIQUE KEY `password` (`password`);

  ");
}
function db()
{
	static $db=null;
	if ($db===null)
	{
		$db=new PDO("mysql:host=localhost","root","123456aB");
		$db->exec("use HDK2016;");
		$db->setAttribute( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
		$db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ); 
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
