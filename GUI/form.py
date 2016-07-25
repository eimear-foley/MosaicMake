#!/usr/bin/env python3

from cgitb import enable
enable()

print("Content-Type: text/html")
print()
print("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--
Design by TEMPLATED
http://templated.co
Released for free under the Creative Commons Attribution License

Name       : RedMarket 
Description: A two-column, fixed-width design with dark color scheme.
Version    : 1.0
Released   : 20140101

-->
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>MosaicMake</title>
		<meta name="keywords" content="" />
		<meta name="description" content="" />
		<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet" />
		<link href="../default.css" rel="stylesheet" type="text/css" media="all" />
		<link href="../fonts.css" rel="stylesheet" type="text/css" media="all" />
		<link rel="icon" href="../jigsaw.png">

		<!--[if IE 6]><link href="default_ie6.css" rel="stylesheet" type="text/css" /><![endif]-->

		<script src="../back_to_top.js" type="text/javascript"></script>
		<script type="text/javascript">

			var request;
			var option;
			var span;

			document.addEventListener('DOMContentLoaded', get_option, false);

			function get_option(){
				span = document.getElementById('span');
				var select = span.firstChild;
				select.addEventListener('click', fillSpan, false);
				
			function fillSpan(){
				option = select.value;
				if option === '1'{
					span.innerHTML = ""

				}




			}
		</script>
	</head>

	<body>
		<a href="#" class="back-to-top"><br>Back to Top</a>
		<div id="header-wrapper" style="height: 35%;">
			<div id="header" class="container">
				<div id="logo">
					<h1 style=" color: white;"> <img src="../jigsaw.png" alt="jigsaw piece" height="25" width="25">  MosaicMake</h1>
				</div>	

				<div id="menu">
					<ul>
						<li class="active"><a href="http://143.239.81.202" accesskey="1" title="">Home</a></li>
					</ul>
				</div>
			</div>
		</div>

		<div id="wrapper">
			<br />
			<div class="container">
				<form action="loading.py" method="post">
					<label for="photos">Choose the number of photos in your mosaic</label>
					<span id="span" style="display: inline-block;"><select name="photos" required>
						<option value="1">20x20 (400)</option>
    					<option value="2">40x40 (1600)</option>
    					<option value="3">50x50 (2500)</option>
    					<option value="4">60x60 (3600)</option>
    					<option value="5">70x70 (4900)</option>
					</select></span>
					<input type="text">
				</form>
			</div>
		</div>
		<div id="copyright" class="container">
			<p>&copy; Untitled. All rights reserved. | released under the <a href="http://templated.co/license">Creative Commons Attribution</a> license | Design by <a href="http://templated.co" rel="nofollow">TEMPLATED</a>.</p>
		</div>
	</body>
</html>
	</body>

</html>
""")
