<?php
if  (isset($_POST['username']) and isset($_POST['password']) and isset($_POST['serialnumber']))
	{
		if (signup($_POST['username'],$_POST['password'],$_POST['serialnumber'])===false)
			echo "Signup failed. Either username or password or serialnumber has been used before. ";
		else
			header("location: ./");
	}
	?> <h2>Sign Up</h2>
<p>Please enter your desired username and password, and the serial number that you received when you purchased our product:</p>
<style>
label {
	float:left;
	width:150px;
	clear:both;
}
input[type='submit'] {
	margin-left:150px;
}
</style>
<form method='post'>
	<label>Username:</label> <input type='text' name='username' /><br/>
	<label>Password:</label> <input type='password' name='password' /><br/>
	<label>Serial Number:</label> <input type='text' name='serialnumber' /><br/>
	<input type='submit' value='Sign Up'/>
</form>
		<a href='./'>Home</a>
	<?php
