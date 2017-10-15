<?php
require_once "config.php";
if (isset($_POST['message']))
{
	$query="INSERT INTO tickets (sessionid,timestamp,title,message) VALUES ('".session_id()."',".time().",'".htmlspecialchars($_POST['title'])."','".htmlspecialchars($_POST['message'])."')";
	$res=db()->exec($query);
}

?>
<style>
.message {
	padding:10px;
	background-color:gray;
	color:white;
	border:3px double black;
	text-indent: -100px;
	margin:10px;
}
.title {
	position:relative;
	top:-20px;
	left:100px;
	padding:1px;
	border:1px solid #555;
	background-color:gray;
}
.smaller {
	color:#DDD;
	font-size:smaller;
}
</style>
<?php
$res=select("*","tickets","sessionid='".session_id()."'","", "timestamp DESC","10");
if ($res)
{
	echo "<h2>Your latest tickets:</h2>";
	foreach ($res as $record)
	{
		echo "<div class='message'>
		<span class='title'><span class='smaller'>(".date("Y-m-d H:i:s",$record->timestamp).") #{$record->ID}</span> {$record->title} </span>
		{$record->message}
		</div>",PHP_EOL;
	}
}
?>
<form method='post' style='border:3px double gray;padding:10px;width:500px;'>
<p>Send a new ticket to the administrators:</p>
	<label>Title:</label>
		<input type='text' name='title' />
		<br/>

	<label>Message:</label>
		<textarea cols='40' rows='5' name='message' ></textarea>
	<br/>
	<label style='visibility: hidden;'>.</label><input type='submit' style='width:150px;' />
</form>
<br/>
<br/>
<a href='./'>Back</a>