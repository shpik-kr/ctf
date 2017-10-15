<?php

@$data=$_POST['data'];


$r=explode("|",$data);
$arr=[];
if ($r)
foreach ($r as $t)
{
	if (strpos($t,"=")===false) continue;
	$arr[explode("=",$t)[0]]=explode("=",$t)[1];
}
if (!isset($arr['username']) or !isset($arr['password']))
	die('0');
if (md5($arr['username'].$arr['password'])!=="b4dae82ae3c7484f725a667e5ecc4e78")
	die("0");

die("1");