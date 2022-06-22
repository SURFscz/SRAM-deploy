var parts = window.location.href.split('?');
var url = parts[0]
var params = parts[1];
var keys = params.split('&');
var l = {};
for (var i=0; i<keys.length; i++) {
  var[k,v] = keys[i].split('=');
  l[k]=v;
}
delete l.acr_values;
var p = [];
for (const [key, value] of Object.entries(l)) {
   p.push(key + "=" + value);
}
var new_params = p.join("&");
var new_url = url + "?" + new_params
var new_url_passwd = new_url + "&acr_values=urn:oasis:names:tc:SAML:2.0:ac:classes:InternetProtocolPassword";
var new_url_mfa = new_url + "&acr_values=https://refeds.org/profile/mfa";
document.write("<a href=\"" + new_url_passwd + "\" id=\"acr_password\">ACR_Password</a><br>");
document.write("<a href=\"" + new_url_mfa + "\" id=\"acr_mfa\">ACR_mfa</a><br>");
