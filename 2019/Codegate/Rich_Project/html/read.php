<div class="container" style="margin-top:120px">
<?php
	if(!isset($_SESSION['ID']))
		die('login first');	

	if(isset($_GET['no']))
	{
		$conn = dbconn("userdata");
		$no = addslashes($_GET['no']);
		$q = "SELECT * FROM board where no='{$no}'";
		$res = mysqli_query($conn,$q);
		$row = mysqli_fetch_assoc($res);
		$title = $row['title'];
		$contents = $row['contents'];
		if($row['secret'] && $row['writer'] !== $_SESSION['ID'])
			$contents = "You are not {$row['writer']}. You can't read this article.";
	}
?>
<form action="./?p=write" method="POST">
  <div class="form-group">
    <label>Title</label>
    <textarea style="resize:none;" class="form-control" name="title" rows="1" readonly><?php echo $title;?></textarea>
  </div>
  <div class="form-group">
    <label>Contents</label>
    <textarea style="resize:none;" class="form-control" name="contents" rows="10" readonly><?php echo $contents;?></textarea>
  </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
