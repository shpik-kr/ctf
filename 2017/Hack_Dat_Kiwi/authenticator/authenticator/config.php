<?php
// ini_set("display_errors",false);
assert(ini_get("max_input_vars")<=1000);
assert(ini_get("max_input_time")=="-1" or ini_get("max_input_time")>=30);
ini_set("max_execution_time","2");
set_time_limit(2);
assert(ini_get("post_max_size")<=2); 
ini_set("memory_limit",(ini_get("post_max_size")*32)."M");

function curl($url,$postparams=[])
{
	$opts=[
		CURLOPT_COOKIEJAR => 'kiwimaster.cookie',
		CURLOPT_COOKIEFILE => 'kiwimaster.cookie',
    	CURLOPT_RETURNTRANSFER => 1,
    	CURLOPT_URL => $url,
    	CURLOPT_USERAGENT => 'Kiwi Master'
	];
	if ($postparams)
	{
		$opts[CURLOPT_POST]=1;
		$opts[CURLOPT_POSTFIELDS]=http_build_query($postparams);
	}
	$curl = curl_init();
	curl_setopt_array($curl, $opts);
	$res = curl_exec($curl);
	curl_close($curl);
	return $res;
}
function url()
{
	return "http://localhost/$_SERVER[REQUEST_URI]";
	return "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

}