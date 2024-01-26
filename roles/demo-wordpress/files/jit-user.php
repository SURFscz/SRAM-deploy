<?php
/*
Plugin Name: JIT User
*/

add_action('login_init', function() {
    // error_log("This is login_init");
    if (isset($_SERVER['HTTP_X_AUTHENTICATED_USER'])) {
        $user = $_SERVER['HTTP_X_AUTHENTICATED_USER'];
        // error_log("user: $user");
        $wp_user = get_user_by('login', $_SERVER['HTTP_X_AUTHENTICATED_USER']);
        // error_log("wp_user: " . print_r($wp_user, true));
        if (!$wp_user) {
          $new_user = array(
            'user_login' => $user,
            'user_pass' => '',
            'role' => 'editor',
          );
          #wp_create_user($user, '');
          wp_insert_user($new_user);
          $wp_user = get_user_by('login', $user);
        }
      //error_log("wp_user: " . print_r($wp_user, true));
      wp_clear_auth_cookie();
      wp_set_auth_cookie($wp_user->ID);
      do_action('wp_login', $wp_user->login, $wp_user);
      wp_safe_redirect(isset($_GET['redirect_to']) ? $_GET['redirect_to'] : admin_url());
      exit;
    }
}, 1);
