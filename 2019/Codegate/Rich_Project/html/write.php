<div class="container" style="margin-top:120px">
<?php
	if(!isset($_SESSION['ID']))
		die('login first');
	if($_SESSION['ID'] === "admin")
		die('Do not write more article. You fired.');
	if(isset($_POST['title']) && isset($_POST['contents']))
	{
		$conn = dbconn("userdata");
		$title = addslashes($_POST['title']);
		$contents = addslashes($_POST['contents']);
		$ID = addslashes($_SESSION['ID']);
		$secret = ($_POST['secret']=="on")?1:0;
		$q = "INSERT INTO board(title,contents,writer,secret) values('{$title}','{$contents}','{$ID}',$secret)";
		mysqli_query($conn,$q);
		mysqli_commit($conn);
		header("Location: ./?p=bbs");
	}
?>
<form action="./?p=write" method="POST">
  <div class="form-group">
    <label>Title</label>
    <textarea style="resize:none;" class="form-control" name="title" rows="1"></textarea>
  </div>
  <div class="form-group">
    <label>Contents</label>
    <textarea style="resize:none;" class="form-control" name="contents" rows="10"></textarea>
  </div>
  <div class="form-check">
    <input type="checkbox" class="form-check-input" name="secret">
    <label class="form-check-label" for="exampleCheck1">Secret</label>
  </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
