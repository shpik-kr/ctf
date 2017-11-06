<?php
	$path = "../T1M3";
	$f = fopen($path,"r");
	$data = fread($f,filesize($path));
	if(!$data)
		$data = "No number has been generated yet.";
?>
    <div class="container">

      <div class="starter-template">
        <h1>Lucky Lo77ery</h1>
        <p class="lead">One chance per 5 Min!<br>If you catch lucky, You will be winner on life!<br> Last generating time : <?= $data?>(on server time.)</p>
	<img src="main.png"/>
      </div>

    </div>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="./dist/js/bootstrap.min.js"></script>
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  

</body>
<!-- leak.tar -->