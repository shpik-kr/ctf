<?php
ini_set("memory_limit",-1);
/**
 * A faster implementation of Levenshtein string distance function. 
 * Also PHP's internal levenshtein only supports 255 characters!
 */
function nti_smart_levenshtein($s1,$s2,$limit=null)
{
	$infinite=9999999;
	$s1=strtolower($s1);$s2=strtolower($s2);
	$n=strlen($s1);$m=strlen($s2);
	if($limit===null)
		$limit=$infinite;
	if(abs($n-$m)>$limit)
		return $infinite;
	if($s1==$s2)
		return 0;
	if(!$n)
		return $m;
	if(!$m)
		return $n;
	$dist=array_fill(0,2,array_fill(0,$m+1,0)); 
	
	$ok=1; $current=1;
	for($i=1;$i<=$m;$i++)
		$dist[0][$i]=$i;
	for($i=1;$i<=$n;$i++)
	{
		$ok=0;
		$dist[$current][0]=$i;
		if($i-$limit>=1)
			$dist[$current][$i-$limit-1]=$infinite;
		for($j=max($i-$limit,1);$j<=min($i+$limit,$m);$j++)
		{
			// if(substr($S1,$i-1,1)==substr($S2,$j-1,1))
			if($s1[$i-1]==$s2[$j-1])
				$dist[$current][$j]=$dist[1-$current][$j-1];
			else
				$dist[$current][$j]=min($dist[1-$current][$j-1],$dist[1-$current][$j],$dist[$current][$j-1])+1;
			if($dist[$current][$j]<=$limit)
				$ok=1;
		}
		if($i+$limit<=$m)
			$dist[$current][$i+$limit+1]=$infinite;
		if(!$ok)
			return $infinite;
		$current=1-$current;
	}
	return $dist[1-$current][$m];
}
/**
 * finds the smallest distance between two strings
 * For example, comparing "hello theres sir" with "yo there" will match "yo there" with "o there".
 * @param  string $short     the smaller string
 * @param  string $long      the longer string (this will be broken down and compared with the short one)
 * @param  float $threshold between 0 and 1. for example, .9 means that dismiss distances that are more than 10%
 * @return array(distance, start, len)
 */
function nti_substring_distance($short,$long,$threshold)
{
	$min=array(strlen($long),0,0);
	for ($j=0;$j<strlen($long);++$j)
	{
		for ($i=1;$i<strlen($long)-$j+1;++$i)
		{
			// echo $j,",",$i,PHP_EOL;
			$str=substr($long,$j,$i);

			//string sizes too different, threshold cannot be observed
			if (abs(strlen($str)-strlen($short))>min(strlen($str),strlen($short))*(1.0-$threshold)) continue; 
			
			if (strlen($str)<256 and strlen($short)<256)
				$t=levenshtein($str,$short);
			else
				$t=nti_smart_levenshtein($str,$short,(int)ceil(strlen($short)*(1.0-$threshold)));
			if ($t<$min[0])
				$min=array($t,$j,$i);
		}
	}
	return $min;
}
/**
 * checks whether an input matches a query or not.
 * Uses string distance, so small changes in the input are still matched
 * @param  string $input 
 * @param  string $query  
 * @return array(similarity 0 to 1, matched portion, position of matched part in query)
 */
function nti($input,$query,$threshold=.51)
{
	list($distance,$start,$length)=nti_substring_distance($input,$query,$threshold);
	$str=substr($query,$start,$length);
	if (!$str)
		return null;
	return ['similarity'=>1-$distance/strlen($input),'match'=>$str,'position'=>$start];
}
