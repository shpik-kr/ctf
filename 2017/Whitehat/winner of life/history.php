   <div class="container">

      <div class="starter-template">
        <h1>ATTEMPT HISTORY</h1>
	<hr>
	<table class="table">
		<thead>
			<tr>
				<th>ROUND</th>
				<th>MY NUMBERS</th>
				<th>TIME</th>
			</tr>
		</thead>
		<tbody>
		<?php
			session_start();
			include 'd6conn.php';
			if($_SESSION['id'])
			{
				$q = "SELECT * FROM ATTEMPT where name='{$_SESSION['id']}'";
				$res = mysqli_query($conn,$q);
				while($row = mysqli_fetch_array($res))
				{
					$q2 = "SELECT * FROM LOG where no={$row['no']} and luckyNumbers='{$row['numbers']}'";
					$res2 = mysqli_query($conn,$q2);
					$row2 = mysqli_fetch_array($res2);
					echo "<tr>";
					echo "<td>{$row['no']}</td>";
					if($row2['luckyNumbers'] == $row['numbers'])
					{
						$path = "../fl4g_Fi13";
						$f = fopen($path,"r");
						$data = fread($f,filesize($path));
						echo "<td>{$data}</td>";
					}
					else
						echo "<td>{$row['numbers']}</td>";
					echo "<td>{$row['date']}</td>";
					echo "</tr>";
				}
			}
			else
				die( "<script> alert('Login first'); location.href='./?p=login'; </script>" );
		?>
		</tbody>
	</table>
      </div>

    </div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="./dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>


</body>