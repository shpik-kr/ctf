<?php

//prevent breaking Lexer
foreach (array($_REQUEST,$_GET,$_POST) as $input) 
	foreach ($input as $in)
		if (!preg_match("/^[a-z\d=\\\"\'(),\s.!?]*$/im", $in,$match))
			die("Bad input: ".htmlspecialchars($in));


require_once __DIR__."/QuickMySqlLexer.php";
function ti_enforce($query)
{
	if (ti_mode&1)	
		pti_enforce($query);
	if (ti_mode&2)
		nti_enforce($query);
}

function pti_enforce($query)
{
	$lexer=new QuickMySqlLexer();
	$lexer->lex($query);
	$markings=$lexer->markings();
	
	require_once __DIR__."/pti.php";
	$pt=pti($query);
	for ($i=0;$i<strlen($query);++$i) 
	//Attack if any SQL critical token (k=Keyword, i=Identifier, @=Symbol, c=Comment) is not PositivelyTainted
		if (($markings[$i]=='k' or $markings[$i]=='i' or $markings[$i]=='@' or $markings[$i]=='c') and $pt[$i]=='0')
			die(sprintf("Attack Detected (PTI:%d)<!--:\n%10s: %s\n%10s: %s\n%10s: %s\n%10s: %s\n-->"
							,$i,"Query",$query,"Markings",$markings,"Match",$pt,"Position",str_repeat(" ",$i)."*"));
}
function nti_enforce($query)
{
	$lexer=new QuickMySqlLexer();
	$lexer->lex($query);
	$markings=$lexer->markings();
	require_once __DIR__."/nti.php";
	$threshold=0.9; //90%+ similarity means match
	$inputs=[$_GET,$_POST,$_COOKIE];
	foreach ($inputs as $input_source)
		foreach ($input_source as $k=>$input)
		{
			if ($res=nti($input,$query,$threshold) and $res['similarity']>=$threshold)
			{
				extract($res);
				//Attack if any SQL critical token (k=Keyword, i=Identifier, @=Symbol, c=Comment) is NegativelyTainted
				//only non-critical tokens can be negatively tainted
				//Attack if any SQL non-critical token () is NegativelyTainted
				for ($i=$position;$i<$position+strlen($match);++$i)
					if ($markings[$i]=='k' or $markings[$i]=='i' or $markings[$i]=='@')
						die(sprintf("Attack Detected (NTI:%d)<!--:\n%10s: %s\n%10s: %s\n%10s: %s\n%10s: %s\n%10s: %.1f%%-->"
							,$i,"Query",$query,"Markings",$markings,"Input",str_repeat(" ",$position).$input,"Match",str_repeat(" ",$position).$match,"Similarity",$similarity*100));

			}
		}
}
function sql_($query)
{
	ti_enforce($query);
	return sql_($query);
}

