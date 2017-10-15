<?php
session_start();
require_once __DIR__."/config.hti.php";
require_once __DIR__."/ti/hti.php";
require_once __DIR__."/db.php";
function select($fields,$tables=array(),$conditions=array(),$groupBy=array(),$orderBy=array(),$limit="")
{
	if (is_array($fields))
		$fields=implode(",",$fields);
	if (is_array($tables))
		$tables=implode(",",$tables);
	if (is_array($conditions))
	{
		array_walk($conditions,function(&$v,$k) { $v="{$k}={$v}";});
		$conditions=implode(" AND ",$conditions);
	}
	if (is_array($groupBy))
		$groupBy=implode(",",$groupBy);
	if (is_array($orderBy))
		$orderBy=implode(",",$orderBy);
	
	$query="SELECT  {$fields}";
	if ($tables)
		$query.=" FROM {$tables}";
	if ($conditions)
		$query.=" WHERE {$conditions}";
	if ($groupBy)
		$query.=" GROUP BY {$groupBy}";
	if ($orderBy)
		$query.=" ORDER BY {$orderBy}";
	if ($limit)
		$query.=" LIMIT {$limit}";
	$res=db()->query($query);
	if (!$res) return false;
	$out=$res->fetchAll(); 
	return $out;
}
?>
<html>
<head>
<style>
label {
	float:left;
	clear:both;
	width:200px;
}
</style>
</head>
<body>
<?php
register_shutdown_function(function(){ 
?>
<div style='font-size:smaller;color:gray;background-color:#EEE;text-align:center;margin:10px auto;padding:3px;'>
	WARNING: This system is protected by a <a href='./hti-ad.php' style='color:inherit;text-decoration: none;'>patented security technology</a>.
Any attempts to exploit this software will be futile.</div> 
</body>
</html>
<?php
});