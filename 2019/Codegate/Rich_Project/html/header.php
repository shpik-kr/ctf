<?php
	session_start();
	include 'dbconn.php';
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>Project Rich</title>

    <link href="/css/bootstrap.min.css" rel="stylesheet">

    <script src="/js/ie-emulation-modes-warning.js"></script>

    <link href="/css/carousel.css" rel="stylesheet">
  </head>
  <body>
    <div class="navbar-wrapper">
      <div class="container">

        <nav class="navbar navbar-inverse navbar-static-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="./?p=home">SCAM</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li><a href="?p=home">Home</a></li>
                <li><a href="?p=info">Info</a></li>
                <li><a href="?p=bbs">Board</a></li>
		<li><a href="?p=market">Market</a></li>
		<?php
			if(!isset($_SESSION['ID']))
				echo '               <li><a href="?p=login">login</a></li>';
			else
				echo '                <li><a href="?p=logout">logout</a></li>';

		?>
                  </ul>
                </li>
              </ul>
            </div>
          </div>
        </nav>

      </div>
    </div>
