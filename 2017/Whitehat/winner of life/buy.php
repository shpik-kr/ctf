<?php
	session_start();
	include 'd6conn.php';
	$round = getRound($conn);
	
?>
<div class="container">
      <div class="starter-template">
        <h1>ROUND : <?=$round?></h1>
        <p class="lead">You can choice 7 numbers.</p>
	<form action="/buy_check.php" method='post'>
	<?php
		for($i = 1; $i<77+1; $i++)
		{
			if($i%11 == 1)
				echo "<pre>";
			echo sprintf('<label><input type="checkbox" name="%d" value="%d">%02d&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>',$i,$i,$i);
			if(!($i %11))
				echo "</pre>";
		}
	?>
		<input type="submit" value="Submit">
	</form>
      </div>

    </div>