<div class="container" style="margin-top:80px">
<?php
	if(isset($_POST['id']) && isset($_POST['pw']) && isset($_POST['ac']))
	{
		$conn = dbconn('userdata');
		$conn2 = dbconn('tradedata');
		$ID = addslashes($_POST['id']);
		$Rules = "/admin/i";
		if(preg_match($Rules,$ID))
			die('"admin" is fobbiden word');
		$PW = sha1(addslashes($_POST['pw']));
		$AC = $_POST['ac'];
		$Rules =""; #File Crakced :p. But you don't need this, right?
		if(substr_count($AC,"'") > 2)
			die('no hack');
		if(preg_match($Rules,$AC))
			die('no hack');
		$q = "INSERT INTO users values('{$ID}','{$PW}','{$AC}')";
		$res = mysqli_query($conn,$q);
		if(mysqli_errno($conn))
			die('error occur, <br>');
		mysqli_commit($conn);
		$q2 = "INSERT INTO user_wallet values('{$ID}',10000,0,'9999-12-31',0)";
		$res2 = mysqli_query($conn2,$q2);
		mysqli_commit($conn2);
		if(mysqli_errno($conn2))
			die('error occur, <br>');
		$_SESSION['ID'] = strtolower($ID);
		header("Location: ./?p=main");
	}

?>

<link href="/css/signin.css" rel="stylesheet">

      <form class="form-signin" action="./?p=reg" method="POST">
        <label for="inputEmail" class="sr-only">ID</label>
        <input type="text" name="id" class="form-control" placeholder="UserID" required="" autofocus="">
        <label for="inputPassword" class="sr-only">Password</label>
	<input type="password" name="pw" class="form-control" placeholder="Password" required="">
	<label for="inputAccount" class="sr-only">Account</label>
        <input type="text" name="ac" class="form-control" placeholder="AccountNumber" required="">
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign up</button>
      </form>

