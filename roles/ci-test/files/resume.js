fragment = window.location.hash.substring(1);
//alert(fragment);
if (fragment) {
  params = fragment.split("&")
  for (let i=0; i < params.length; i++) {
    var p = params[i].split("=");
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = p[0];
    input.value = p[1];
    document.forms['oidc'].appendChild(input);
  }
  document.forms['oidc'].submit();
}
