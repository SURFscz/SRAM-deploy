<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link href="/auth.css" rel="stylesheet">
    <title>SRAM Demo SP</title>
</head>
<body>
<?php
session_start();

# supported environments; should correspond to configured SPs
$ENVS = array("test","test2", "acc","prd");
$FORMATS = array("table", "json", "raw");

$SUPPORTED = array(
    'cn',
    'displayName',
    'givenName',
    'sn',
    'mail',
    'eduPersonUniqueId',
    'subject-id',
    'voPersonID',
    'voPersonExternalID',
    'uid',
    'eduPersonPrincipalName',
    'eduPersonScopedAffiliation',
    'voPersonExternalAffiliation',
    'eduPersonEntitlement',
    'sshPublicKey',
);

$UNSUPPORTED = array(
    'eduPersonAssurance',
    'schacHomeOrganization',
);

# sanitize user input
$env = $_SERVER['PATH_INFO'];
if (!in_array($env, $ENVS)) {
    http_response_code(404);
    die();
}

# get and store output format
if ($format = @$_GET['format']) {
    if (in_array($format, $FORMATS)) {
        $_SESSION['format'] = $format;
    } else {
        $format = '';
    }
} else {
    $format = $_SESSION['format'];
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

if ($format=="raw") {
    print('<div id="raw">');
    print('<h1>Raw attributes</h1>');
    print('<code style="white-space: pre;">');
    print_r($user_attr);
    print('</code>');
    print('</div>');
    exit();
}

if ($format=="json") {
    print('<pre id="data">');
    print(json_encode($user_attr, JSON_PRETTY_PRINT));
    print('</pre>');
    exit();
}

print('<div id="known">');
print('<h1>Known attributes</h1>');
print('<table class="redTable">');
print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
foreach ($SUPPORTED as $attr) {
    print('<tr>');
    print("<td>{$attr}</td>"); print("\n");
    print('<td>');
    if (array_key_exists($attr, $user_attr)) {
        sort($user_attr[$attr]);
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


print('<div id="unsupported">');
print('<h1>Unsupported attributes</h1>');
print('<table class="redTable">');
print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
foreach ($UNSUPPORTED as $attr) {
    print('<tr>');
    print("<td>{$attr}</td>"); print("\n");
    print('<td>');
    if (array_key_exists($attr, $user_attr)) {
        sort($user_attr[$attr]);
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

$known_attr = array_merge(
    $SUPPORTED,
    $UNSUPPORTED,
);

$unknown_attr = array_diff( array_keys($user_attr), $known_attr );
if ( !empty($unknown_attr) ) {
    print('<div id="unknown">');
    print('<h1>Unknown attributes</h1>');
    print('<table class="redTable">');
    print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
    foreach ($unknown_attr as $attr) {
        print('<tr>');
        print("<td>{$attr}</td>"); print("\n");
        print('<td>');
        foreach ($user_attr[$attr] as $val) {
            sort($user_attr[$attr]);
            print('<span class="attr_val">');
            print($val);
            print('</span>');
        }
        print('</td>'); print("\n");
        print('</tr>'); print("\n");
    }
    print('</table>');
    print('</div>');
}

echo("<br>\n");
$url = $as->getLogoutURL("/");
printf('<div><a href="%1$s">logout</a></div>', htmlspecialchars($url));

?>
</body>
</html>
