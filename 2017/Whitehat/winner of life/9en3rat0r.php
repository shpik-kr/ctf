<?php
function generator()
{
	$PATH = "/var/www/s3cre7_fi1e";
	$init_seed = 0;
	if(!file_exists(realpath($PATH)))
	{
		$init_seed = $seed = intval(uniqid(),10);
		$f = fopen($PATH,"w");
		fwrite($f,$init_seed);
		fclose($f);
	}
	
	$f = fopen($PATH,"r");
	$data = fread($f,filesize($PATH));
	$init_seed = $seed = intval($data,10);

	srand($init_seed);
	for( $i=0; $i<$init_seed%100; $i++)
	{
		$seed = rand() * rand();
		srand($seed);
		$tmp = rand()*rand();
		$length = strlen($tmp);
		$cutting = (int)($length/4);
		$tmp2= substr($seed,$cutting,$length-$cutting*2);
		$seed = $tmp2*$tmp2;
	}
	$ret = array(7);
	$new_seed = 0;
	for( $i=0; $i<7; $i++)
	{	$new_seed = rand();
		$number = ($new_seed%77)+1;
		if(in_array($number,$ret))
		{
			$i--;
			continue;
		}
		$ret[$i] = $number;
	}
	$f = fopen($PATH,"w");
	fwrite($f,$new_seed);
	fclose($f);
	return $ret;
	
}
?>