<?php
foreach ($_SERVER as $claim => $value) {
    if (substr($claim, 0, 4) === 'OIDC') {
        echo "<p>" . substr($claim, 5) . ": $value</p>\n";
    }
}
//phpinfo();

