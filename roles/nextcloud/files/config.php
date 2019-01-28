<?php
$CONFIG = array (
  'htaccess.RewriteBase' => '/',
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'apps_paths' =>
  array (
    0 =>
    array (
      'path' => '/var/www/html/apps',
      'url' => '/apps',
      'writable' => false,
    ),
    1 =>
    array (
      'path' => '/var/www/html/custom_apps',
      'url' => '/custom_apps',
      'writable' => true,
    ),
  ),
  'passwordsalt' => 'IQNtcmNvCWr2AjmmXJGxqp22hTG7Pg',
  'secret' => 'tPXzEQ5Xp49GsjNcrcLMP/AlNbNAaV6U6QpM1XnGzUQeqt9b',
  'trusted_domains' =>
  array (
    0 => 'localhost',
  ),
  'datadirectory' => '/var/www/html/data',
  'dbtype' => 'sqlite3',
  'version' => '15.0.2.0',
  'overwrite.cli.url' => 'http://localhost',
  'dbname' => 'nextcloud.sqlite',
  'installed' => true,
  'instanceid' => 'ocfoukzhokvl',
);
