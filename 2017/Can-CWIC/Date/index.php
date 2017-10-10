<!DOCTYPE HTML>

<html>
  <head>
    <title>The Date of Today</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
    <style>
      body, html { height: 100%; font-family: monospace;}
      body { background-color: #f0f0dd; padding-top: 5%; }
	.panel-heading, .panel-footer { background-color: #cccc99 !important; color=blue; }

      .centered {
	position: relative;
	left: 50%;
	/* bring your own prefixes */
	transform: translate(-50%, 0);
	max-width: 70%;
      }

    </style>
  </head>
  <body>


    <div class="panel panel-default centered">
      <div class="panel-heading"><h1>The Date of Today</h1></div>
      <div class="panel-body">
<h1>
<?php
$cmd = 'date';
$fmt = isset($_GET['fmt'])?$_GET['fmt']:"";
if (isset($_GET['rfc'])) {
	$cmd = $cmd . ' -R';
	$rfcx = ' checked';
}
if ($fmt != "") {
	$cmd = $cmd . ' +' . $fmt;
	$fmtx = ' value="' . $fmt . '"';

}
$cmd = escapeshellcmd($cmd);
$res = system($cmd . " 2>&1");

include 'varflag.php';
if ($res === $date && strpos($fmt, 'easter') != false) {
	echo "<b style='color:red'>$flag</b>";
}
?>
</h1>
	<br>
	<form action="index.php" method="GET">
	<div class="form-group">
	  <label>Format : </label>
	  <input type="text" name="fmt" class="form-control"<?=$fmtx?>></input>
	  </div>
	<div class="checkbox">
	<label><input type="checkbox" name="rfc"<?=$rfcx?>>RFC 2822</label>
	  </div>


	  <input type="submit" class="pull-right btn btn-primary"
	    value="Update"></input>
	</form>
	<br>

<p>FORMAT controls the output. Interpreted sequences are:</p>
<dl compact>
<dt>%%
<dd>a literal %
<dt>%a
<dd>locale's abbreviated weekday name (e.g., Sun)
<dt>%A
<dd>locale's full weekday name (e.g., Sunday)
<dt>%b
<dd>locale's abbreviated month name (e.g., Jan)
<dt>%B
<dd>locale's full month name (e.g., January)
<dt>%c
<dd>locale's date and time (e.g., Thu Mar 3 23:05:25 2005)
<dt>%C
<dd>century; like %Y, except omit last two digits (e.g., 20)
<dt>%d
<dd>day of month (e.g, 01)
<dt>%D
<dd>date; same as %m/%d/%y
<dt>%e
<dd>day of month, space padded; same as %_d
<dt>%F
<dd>full date; same as %Y-%m-%d
<dt>%g
<dd>last two digits of year of ISO week number (see %G)
<dt>%G
<dd>year of ISO week number (see %V); normally useful only with %V
<dt>%h
<dd>same as %b
<dt>%H
<dd>hour (00..23)
<dt>%I
<dd>hour (01..12)
<dt>%j
<dd>day of year (001..366)
<dt>%k
<dd>hour ( 0..23)
<dt>%l
<dd>hour ( 1..12)
<dt>%m
<dd>month (01..12)
<dt>%M
<dd>minute (00..59)
<dt>%n
<dd>a newline
<dt>%N
<dd>nanoseconds (000000000..999999999)
<dt>%p
<dd>locale's equivalent of either AM or PM; blank if not known
<dt>%P
<dd>like %p, but lower case
<dt>%r
<dd>locale's 12-hour clock time (e.g., 11:11:04 PM)
<dt>%R
<dd>24-hour hour and minute; same as %H:%M
<dt>%s
<dd>seconds since 1970-01-01 00:00:00 UTC
<dt>%S
<dd>second (00..60)
<dt>%t
<dd>a tab
<dt>%T
<dd>time; same as %H:%M:%S
<dt>%u
<dd>day of week (1..7); 1 is Monday
<dt>%U
<dd>week number of year, with Sunday as first day of week (00..53)
<dt>%V
<dd>ISO week number, with Monday as first day of week (01..53)
<dt>%w
<dd>day of week (0..6); 0 is Sunday
<dt>%W
<dd>week number of year, with Monday as first day of week (00..53)
<dt>%x
<dd>locale's date representation (e.g., 12/31/99)
<dt>%X
<dd>locale's time representation (e.g., 23:13:48)
<dt>%y
<dd>last two digits of year (00..99)
<dt>%Y
<dd>year
<dt>%z
???LINES MISSING
