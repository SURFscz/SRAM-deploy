<h1>OIDC RP Test</h1>
<?php
foreach ($_SERVER as $key => $value) if (substr($key,0,4) == "OIDC") echo "<p>" . substr($key,5) . ": $value</p>\n";
