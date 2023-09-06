<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="/bootstrap.min.css" rel="stylesheet">
    <link href="/demosp.css" rel="stylesheet">

    <title>SURF Research Access Management Demo SP</title>
</head>
<body>
<?php
session_start();

# supported environments; should correspond to configured SPs
$ENVS = array("test","acc","prd");
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
    'userid',
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
    print('</body></html>');
    exit();
}

if ($format=="json") {
    print('<pre id="data">');
    print(json_encode($user_attr, JSON_PRETTY_PRINT));
    print('</pre>');
    print('</body></html>');
    exit();
}
?>
<nav class="navbar navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">SRAM Demo SP</a>
    </div>
</nav>
<main>
<div class="container">

<div class="card mt-4">
    <div class="card-header">Supported attributes</div>
    <div class="card-body d-flex flex-column">
<?php

print('<div class="table-responsive">');
print('<table class="table">');
print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
foreach ($SUPPORTED as $attr) {
    print('<tr>');
    print("<th>{$attr}</th>"); print("\n");
    print('<td class="font-monospace text-nowrap">');
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

?>
</div>
</div>

<div class="card mt-4">
    <div class="card-header">Unsupported attributes</div>
    <div class="card-body d-flex flex-column">
<?php
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
?>
</div>
</div>

<div class="card mt-4">
    <div class="card-header">Unknown attributes</div>
    <div class="card-body d-flex flex-column">
<?php

$known_attr = array_merge($SUPPORTED, $UNSUPPORTED);
$unknown_attr = array_diff( array_keys($user_attr), $known_attr );

if ( !empty($unknown_attr) ) {
    print('<div class="table-responsive" id="unknown">');
    print('<table class="table">');
    print('<thead><tr><th>Attribute</th><th>Value</th></thead>'); print("\n");
    foreach ($unknown_attr as $attr) {
        print('<tr>');
    print("<th>{$attr}</th>"); print("\n");
    print('<td class="font-monospace text-nowrap">');
        foreach ($user_attr[$attr] as $val) {
            sort($user_attr[$attr]);
        print('<div class="attr_val">');
            print($val);
            print('</span>');
        }
        print('</td>'); print("\n");
        print('</tr>'); print("\n");
    }
    print('</table>');
    print('</div>');
};
?>
</div>
</div>

<?php
$url = $as->getLogoutURL("/");
printf('<div class="mt-4"><a href="%1$s" class="btn btn-primary">logout</a></div>', htmlspecialchars($url));
?>
</div></div>
</main>
</body>
</html>
