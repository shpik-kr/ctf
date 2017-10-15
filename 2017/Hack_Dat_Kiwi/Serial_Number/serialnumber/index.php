<?php
if  (isset($_POST['username']) and isset($_POST['password']))
{
	if (login($_POST['username'],$_POST['password'])===false)
		echo "Login failed. ";
	else
		header("location: ");
}

if (loggedin())
{
	echo "Welcome ".user()->username.".<br/> There's not much to do around here. (Unless you've used a valid serial number)<br/>";
	if (isadmin(user()))
		echo "The flag is: ",sql("select * from flag")[0]->flag,PHP_EOL;
	echo "<br/><br/><a href='./logout.php'>Logout</a>";
}
else
{
	
	?> Please login:<br/>
	<form method='post'>
		<label>Username:</label> <input type='text' name='username' /><br/>
		<label>Password:</label> <input type='password' name='password' /><br/>
		<input type='submit' value='Login'/>
	</form>
		<a href='signup.php'>Sign Up</a>
	<?php
}