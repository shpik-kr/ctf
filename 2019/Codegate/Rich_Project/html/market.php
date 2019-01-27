<div class="container" style="margin-top:120px">
<?php 
	if(!isset($_SESSION['ID']))
		die('login first');
	if($_SESSION['ID'] =="admin")
		die('Fobbiden account');
	$conn = dbconn('tradedata');
	$q = "SELECT * FROM user_wallet where id='{$_SESSION['ID']}'";
	$res = mysqli_query($conn,$q);
	$row = mysqli_fetch_assoc($res);
	$limit = 24;

	$q2 = "SELECT * FROM (select * from coin_price order by Date desc limit {$limit})a order by Date asc";
	$res2 = mysqli_query($conn,$q2);
	$priceArr = array();
	$dateArr = array();
	while($row2 = mysqli_fetch_assoc($res2))
	{
		array_push($priceArr,$row2['price']);
	}
	$last = count($priceArr)-1;
	$priceData = implode(",",$priceArr);
?>

<script src="/js/echarts.simple.min.js"></script>
	<div id='main' style="margin-top:80px; height:500px;">
    <script type="text/javascript">
        var myChart = echarts.init(document.getElementById('main'));
	var option = {
    xAxis: {
        type: 'category',
		data: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    },
    yAxis: {
        type: 'value'
    },
    series: [{
    data: [<?php echo $priceData;?>],
        type: 'line'
    }]
};

        myChart.setOption(option);
    </script>
	</div>
	<div class="col-md-6 col-md-offset-5">
<?php
	### if reserv is exists
	$q = "SELECT * FROM coin_price where Date like '%{$row['reserv']}%' order by Date limit 1";
	$res = mysqli_query($conn,$q);
	$row2 = mysqli_fetch_assoc($res);
	if($row['cash'] < $row2['price']*$row['amount'])
		echo "Not enough cash to buy SCAM coin. your reservation is failed..</br>"; 
	else
	{
		$cash = $row['cash'] - ($row2['price'] * $row['amount']);
		$coin = $row['coin'] + $row['amount'];
		$q = "UPDATE user_wallet set amount=0, reserv='9999-12-30',cash='{$cash}', coin='{$coin}' where id='{$_SESSION['ID']}'";
		mysqli_query($conn,$q);
		mysqli_commit($conn);

		#refresh..
		$q = "SELECT * FROM user_wallet where id='{$_SESSION['ID']}'";
	        $res = mysqli_query($conn,$q);
	        $row = mysqli_fetch_assoc($res);
	}


?>
	<b>Current coin price : <?php echo $priceArr[$last];?> gold</b>
	</div>
<br><br>
	<div class="col-md-4">
		<link href="/css/signin.css" rel="stylesheet">
		<form class="form-signin" action="./?p=buy" method="POST">
			<label>Your Balance : <?php echo $row['cash'];?> gold</label>
		        <input type="text" name="amount" class="form-control" placeholder="amount" required=""><br>
		        <button class="btn btn-lg btn-primary btn-block" type="submit">Buy</button>
	        </form>
	</div>
	<div class="col-md-4">
		<form class="form-signin" action="./?p=sell" method="POST">
                        <label>Your Coins : <?php echo $row['coin'];?>SCAM.</label>
                        <input type="text" name="amount" class="form-control" placeholder="amount" required=""><br>
                        <button class="btn btn-lg btn-danger btn-block" type="submit">Sell</button>
		</form>
	</div>
	<div class="col-md-4">
		<form class="form-signin" action="./?p=reserv" method="POST">
                        <label>Your Balance : <?php echo $row['cash'];?> gold</label>
                        <input type="text" name="amount" class="form-control" placeholder="amount" required=""><br>
			<input type="text" name="date" class="form-control" placeholder="<?php echo date("Y-m-d",time());?>" required=""><br>
                        <button class="btn btn-lg btn-info btn-block" type="submit">Reserve</button>
                </form>
	</div>
