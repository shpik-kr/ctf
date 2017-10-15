<?php
/**
 * String tokens are exactly as they appear in the file, e.g "hello\tthere".
 * This function converts them to actual strings, e.g hello 	there
 */
function pti_parse_string($string) 
{
	$convert=array('\n'=>"\n",'\r'=>"\r",'\t'=>"\t",'\v'=>"\v",'\e'=>"\e",'\f'=>"\f",'\\'=>"\\",'\"'=>"\"");
	$res=strtr($string,$convert);
	$len=strlen($res);
	if ($len>=2) 
	if (($res[0]=="'" and $res[$len-1]=="'") or ($res[0]=='"' and $res[$len-1]=='"')) 
		$res=substr($res,1,$len-=2);
	return $res;
}
/**
 * retrieves all constant literal strings that exist in the PHP source code file
 * @param  string $file 
 * @return array       list of strings
 */
function pti_constant_strings($file)
{
	if (dirname($file)==__DIR__) return array();
	$res=array();
	$phpcode=file_get_contents($file);
	$tokens=token_get_all($phpcode);
	$count=0;
	foreach ($tokens as $token)
	{
		$temp=null;
		if (is_array($token))
		{
			if ($token[0]==T_CONSTANT_ENCAPSED_STRING)
				$temp=pti_parse_string($token[1]);
			elseif($token[0]==T_ENCAPSED_AND_WHITESPACE)
				$temp=pti_parse_string($token[1]);
			elseif ($token[0]==T_CONCAT_EQUAL);
		}
		if ($temp!==null)
			$res[$file.":".$token[2]." (".(++$count).")"]=$temp;
	}
	$res=array_unique($res); //remove duplicates
	$res=array_filter($res); //remove null and false entries
	return $res;
}
/**
 * Finds all string fragments in current project (except files in ti folder)
 * @return array string fragments
 */
function pti_fragments()
{
	static $fragments=null;
	if ($fragments) return $fragments;
	$cache_file=__DIR__."/pti_fragments.txt";
	#TODO: uncomment these for fragment cache
	// if (file_exists($cache_file) and filemtime($cache_file)>=filemtime(__FILE__))
	// 	return $fragments=unserialize(file_get_contents($cache_file));

	$files=get_included_files();
	$root=dirname(array_reduce($files, function ($carry,$item) { if (strlen(dirname($item))<strlen(dirname($carry))) return $item; else return $carry;},__DIR__));
	$fragments=[];
	foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root)) as $file)
	{
		if (dirname($file)==__DIR__) continue; //exclude HTI folder
		if (strlen($file)>3 and substr($file,-4)==".php")
		{
			$res=pti_constant_strings($file);
			$fragments=array_merge($fragments,$res);
		}
	}
	usort($fragments, function ($s1,$s2) {return strlen($s1)<strlen($s2);}); //sort large to small
	@file_put_contents($cache_file,serialize($fragments));
	return $fragments;
}
/**
 * Builds a string using the fragments available (just like a puzzle)
 * @param  string $query 
 * @return array        an array that has either 0 or a number bigger than zero for each char in query. zero means no match.
 */
function pti_construct($query)
{
	$match=array_fill(0,strlen($query),0);
	foreach (pti_fragments() as $k=>$fragment)
	{
		if (strlen($fragment)==1 and strpos(" !@#$%^&*()./\\'][}{><,-=_+",$fragment)===false) continue;
		$index=0;
		while ( ($pos=strpos($query, $fragment,$index))!==false)
		{
			$index=$pos+strlen($fragment);
			$flag=true;
			for ($i=0;$i<strlen($fragment) and $flag;++$i)
				if ($match[$i+$pos]!=0) $flag=false;
			if (!$flag) continue;
			// echo $k,": ",$fragment, "(",$pos,")",PHP_EOL;
			for ($i=0;$i<strlen($fragment);++$i)
				 $match[$i+$pos]++;
		}
	}
	return $match;
}
/**
 * Uses PTI to construct a query. Returns a string of 0s and 1s, 0s for non-matched and 1 for matched.
 */
function pti($query)
{
	$match=pti_construct($query);
	return implode("",array_map(function($x){ return $x==0?"0":"1";},$match));
}