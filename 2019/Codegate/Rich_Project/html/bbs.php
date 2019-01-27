<div class="container" style="margin-top:120px">
<?php 
	if(!isset($_SESSION['ID']))
		die('login first');
	$conn = dbconn('userdata');
?>
	<table class="table table-hover">
		<thead>
			<tr>
				<th style="width:10%">No</th>
				<th>Title</th>
				<th style="width:20%">Writer</th>
			</tr>
		</thead>
		<tbody>
		<tr>
		<td>NOTICE</td>
		<td><a href="./?p=read&no=-1">TOP SECRET</a><span style='color:red'>(s)</span></td>
		<td><span style='color:white'>admin</span></td>
		<?php
			if(!isset($_GET['page']))
				header("Location: ./?p=bbs&page=1");
			$page = ((int)addslashes($_GET['page']/10)-1)*10;
			if($page<-1)
				$page = 0;
			if($page>10)
				$page = 0;
			$limit = ($_GET['page']-1)*10;
			$q = "SELECT * FROM board where no>0 order by no desc limit {$limit},10";
			$res = mysqli_query($conn,$q);
			while($row = mysqli_fetch_array($res))
			{
				$secret = "";
				if($row['secret'])
					$secret = "<span style='color:red'>(s)</span>";
				echo "<tr>";
				echo "<td>{$row['no']}</td>";
				echo "<td><a href=./?p=read&no={$row['no']}>{$row['title']}</a>{$secret}</td>";
				echo "<td>{$row['writer']}</td>";
				echo "</tr>";
			}
		?>
		</tbody>
		<hr/>
	</table>
	<a class="btn btn-default pull-right" href="./?p=write">Write</a>
	<div class="text-center">
		<ul class="pagination">
			<?php
				for($i=1;$i<=10;$i++)
				{
					$numbering = $page+$i;
					echo "<li><a href='./?p=bbs&page={$numbering}'>{$numbering}</a></li>";
				}
			?>
		</ul>
	</div>
