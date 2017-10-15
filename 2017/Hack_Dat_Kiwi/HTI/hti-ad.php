<?php
if (isset($_GET['download']))
{
	header("Content-type: application/force-download");
	header("Content-disposition: attachment;filename=hti.zip");
	readfile("hti.zip");
	die();
}
?>
<h1>Hybrid Taint Inference</h2>
<p>Hybrid Taint Inference is a new, patented automated injection prevention security mechanism. It is very fast, secure and easy to deploy.
	It does not require code modification, code change, training, or etc. Fully automated right out of the box, with 99.99% accuracy.</p>

<p>Hybrid taint inference is based on taint inference, a new taint-based method succeeding taint tracking. 
	It infers taint between input (user-input, which is tainted) and output (query or other injectable string)
	instead of tracking it throughout the application execution (which is slow and inaccurate).</p>

<p>Basically Hybrid Taint Inference (HTI) is the combination of Negative Taint Inference (NTI) and Positive Taint Inference (PTI).</p>

<h2>Negative Taint Inference</h2>
<p>Negative taint inference works by correlating input with output. It finds strings that are similar to input, in the output. 
	If the similarity is above a certain threshold, it marks that part of the output as negatively tainted (=dangerous).</p>

<p>It typically uses Levenshtein edit distance algorithm to figure out how different two strings are, but any algorithm should work. 
	A low threshold (e.g 50%) will result in high false positives, whereas a high threshold (e.g 90%) is susceptible to edit-distance attacks.</p>

<p>As you can see in the figure below, when the user input is <strong>1' OR 1='1</strong>, and the same string is found in the output, NTI
	negatively tains that part of the output (minus signs under it).</p>

<p>When critical keywords of the output string are negatively tainted, it means that an attack is happenning. To figure out which
	parts of the output string are critical keywords, a simple lexer for that grammer will suffice (e.g SQL lexer).</p>

<div style='text-align:center;'>
<img src='taint-markings.jpg' border='1' />
<br/>
Sample taint markings for NTI and PTI.
</div>

<h2>Positive Taint Inference</h2>
<p>Positive taint inference works similar to NTI, but differently. Instead of inferring the taint between negative taint (user input) and the output,
	it infers taint between positive taint (application strings) and output.</p>
<p>To do this, PTI needs to know what strings literals exist in an application. It can scan the application files, lex them and extract
	the string literals (fragments). Then whenever an output is sent, it tries to build different parts of that output with fragments.
	Every part that is built, is positively tainted (trusted). The remaining parts are untrusted.</p>
<p>If a critical keyword exists in the untrusted section, a possible attack is happenning. You can see this in the above figure as well.
	In the figure, we assume that the + parts are strings that existed inside the application.</p>


<h2>Test HTI</h2>
<p>We have a simple implementation of HTI for PHP and MySQL that automatically prevents SQL injection attacks prepared for you to study and test.
	Just modify the config.hti.php file, and set the constant to 1 for PTI, 2 for NTI and 3 for HTI protection. The app has multiple
	SQL injection vulnerabilities which are protected by HTI.</p>


<br/>
<a href='?download'>Download a sample!</a>
