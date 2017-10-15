<?php
require_once __DIR__."/config.php";
if (!loggedin()) header("location: ./");

?>	<h2>Change Password</h2><br/>
<?php
echo "Welcome {$_SESSION['login']['username']}.<br/><br/>";
if  (isset($_POST['oldpass']) and isset($_POST['newpass']))
	{
		if (changepass($_POST['oldpass'],$_POST['newpass'])===false)
			echo "Change password failed. Your new password is probably the same as your old one(s), or is less than 8 characters.";
		else
			echo "Change password successfull. ";
	}
?>
<br/>
<br/>
<form method='post'>
	<label>Old Password:</label> <input type='password' name='oldpass' /><br/>
	<label>New Password:</label> <input type='password' name='newpass' /><br/>
	<input type='submit' value='Change'/>
</form>
		<a href='./'>Home</a>
	<?php
