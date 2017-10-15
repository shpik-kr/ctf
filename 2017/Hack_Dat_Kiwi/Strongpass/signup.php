<?php

if  (isset($_POST['username']) and isset($_POST['password']))
	{
		if (signup($_POST['username'],$_POST['password'])===false)
			echo "Signup failed. ";
		else
			header("location: ./");
	}
	?> Sign Up:<br/>
<form method='post'>
	<label>Username:</label> <input type='text' name='username' /><br/>
	<label>Password:</label> <input type='password' name='password' /><br/>
	<input type='submit' value='Sign Up'/>
</form>
		<a href='./'>Home</a>
	<?php
