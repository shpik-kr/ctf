    <div class="container">

      <div class="starter-template">
        <h1>Statistics</h1>
	<p class="lead">
	<?php
		include 'd6conn.php';
		$no = $_GET['no'];
		if(!$no)
			$no =1;
		### Filtering ###
		$gfw ="/dump|out|sub|in|[+%><!=^|~-]|or|and|lef|rig|conv|if|case|equ|exp|like|sleep|bench|sound|bin|hex|oct|asc|cha|base|not|min|att|acc|whe/i";
		if(preg_match($gfw,$no))
			die("DO NOT INPUT FOBBIDEN KEYWORD!");

		$q = "SELECT * FROM LOG where no={$no}";
		$row = mysqli_fetch_array(mysqli_query($conn,$q));
		if(!is_numeric($row['no']))
			die("'Round' is must be Intiger. not null, not char, not string.");
		$round = $row['no'];
		$winners = explode(",",$row['winners']);
		$winnercount = count($winners);
		if(count($winners) == 1)
		{
			if($winners[0] == "")
				$winnercount = 0;
		}
		echo "ROUND : {$round}<br>";
		echo "WINNER : {$winnercount}";
	?>
	</p>	
      </div>

    </div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="./dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>


</body>