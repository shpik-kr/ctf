<?php
	if(isset($_POST['id']) && isset($_POST['pw']) && isset($_POST['ac']))
	{
		$conn = dbconn('userdata');
		$ID = addslashes($_POST['id']);
		$PW = sha1(addslashes($_POST['pw']));
		$AC = addslashes($_POST['ac']);
		$q = "SELECT * FROM users where id='{$ID}' and pw='{$PW}' and ac='{$AC}'";
		$res = mysqli_query($conn,$q);
		$row = mysqli_fetch_array($res);
		if($row != NULL)
		{
			$_SESSION['ID'] = strtolower($row['id']);
			header("Location: ./?p=main");
			die("");
		}
		header("Location: ./?p=login");
	}

?>
<link href="/css/signin.css" rel="stylesheet">
<div class="container" style="margin-top:80px">

      <form class="form-signin" action="./?p=login" method="POST">
        <input type="text" name="id" class="form-control" placeholder="UserID" required="" autofocus="">
        <label for="inputID" class="sr-only">ID</label>
	<label for="inputPassword" class="sr-only">Password</label>
	<input type="password" name="pw" class="form-control" placeholder="Password" required="">
	<label for="inputAccount" class="sr-only">Account No.</label>
        <input type="text" name="ac" class="form-control" placeholder="AccountNumber" required="">
        <div class="checkbox">
          <label>
            <a href="./?p=reg">Sign up</a>
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
      </form>

