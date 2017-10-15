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
	echo "Welcome {$_SESSION['login']['username']}.<br/> There's not much to do around here.";
	echo "<br/><br/><a href='./change.php'>Change Password</a>";
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