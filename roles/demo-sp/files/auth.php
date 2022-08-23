<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link href="/auth.css" rel="stylesheet">
    <title>SRAM Demo SP</title>
</head>
<body>
<?php

# supported environments; should correspond to configured SPs
$ENVS = array("test","acc","prd");

$ATTRIBUTES = array(
    'subject-id',
    'eduPersonUniqueId',
    'voPersonExternalID',
    'uid',
    'eduPersonPrincipalName',
    'displayName',
    'givenName',
    'sn',
    'mail',
    'eduPersonScopedAffiliation',
    'voPersonExternalAffiliation',
    'eduPersonEntitlement',
    'sshPublicKey',
    'voPersonStatus',
);

$RAW = 0;

# sanitize user input
$env = $_SERVER['PATH_INFO'];
if (!in_array($env, $ENVS)) {
    http_response_code(404);
    die();
}

#phpinfo();

# Load SimpleSaml library
require_once("../simplesaml/lib/_autoload.php");

# Get service provider and authenticate
$as = new SimpleSAML\Auth\Simple($env);
$as->requireAuth();

# double check
if(!$as->isAuthenticated()) {
    $as->login(array(
        'ReturnTo' => $_SERVER['REQUEST_URI']
    ));
    die();
}

$user_attr = $as->getAttributes();

if ($RAW) {
    print('<div id="raw">');
    print('<h1>Raw attributes</h1>');
    print('<code style="white-space: pre;">');
    print_r($user_attr);
    print('</code>');
    print('</div>');
}


print('<div id="known">');
print('<h1>Known attributes</h1>');
print('<table class="redTable">');
print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
foreach ($ATTRIBUTES as $attr) {
    print('<tr>');
    print("<td>{$attr}</td>"); print("\n");
    print('<td>');
    if (array_key_exists($attr, $user_attr)) {
        foreach ($user_attr[$attr] as $val) {
            print('<div class="attr_val">');
            print($val);
            print('</div>');
        }
    } else {
        print('<span class="not_found">not present</span>');
    }
    print('</td>'); print("\n");
    print('</tr>'); print("\n");
}
print('</table>');
print('</div>');



$unknown_attr = array_diff( array_keys($user_attr), $ATTRIBUTES);
print('<div id="unknown">');
print('<h1>Unknown attributes</h1>');
print('<table class="redTable">');
print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
foreach ($unknown_attr as $attr) {
    print('<tr>');
    print("<td>{$attr}</td>"); print("\n");
    print('<td>');
    foreach ($user_attr[$attr] as $val) {
        print('<span class="attr_val">');
        print($val);
        print('</span>');
    }
    print('</td>'); print("\n");
    print('</tr>'); print("\n");
}
print('</table>');
print('</div>');

$url = $as->getLogoutURL("/");
printf('<div><a href="%1$s">logout</a></div>', htmlspecialchars($url));

?>
</body>
</html>
