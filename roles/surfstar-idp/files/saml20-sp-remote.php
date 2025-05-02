<?php

$metadata['https://engine.test.surfconext.nl/authentication/sp/metadata'] = array (
    'entityid' => 'https://engine.test.surfconext.nl/authentication/sp/metadata',
    'metadata-set' => 'saml20-sp-remote',
    'AssertionConsumerService' => array ( 0 =>
        array (
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
            'Location' => 'https://engine.test.surfconext.nl/authentication/sp/consume-assertion',
            'index' => 0,
        ),
    ),
    'attributes.NameFormat' => 'urn:oasis:names:tc:SAML:2.0:attrname-format:uri',
    'keys' => array ( 0 =>
        array (
            'encryption' => false,
            'signing' => true,
            'type' => 'X509Certificate',
            'X509Certificate' => 'MIIEATCCAumgAwIBAgIULxKkZBLB4NcvlnV253iUmoreAqIwDQYJKoZIhvcNAQELBQAwgYoxCzAJBgNVBAYTAk5MMRAwDgYDVQQIDAdVdHJlY2h0MRAwDgYDVQQHDAdVdHJlY2h0MRUwEwYDVQQKDAxTVVJGbmV0IEIuVi4xEzARBgNVBAsMClNVUkZjb25leHQxKzApBgNVBAMMImVuZ2luZS50ZXN0LnN1cmZjb25leHQubmwgMjAxODAyMDgwHhcNMTkwMjA4MTI0OTE1WhcNMjMxMTEzMTI0OTE1WjCBijELMAkGA1UEBhMCTkwxEDAOBgNVBAgMB1V0cmVjaHQxEDAOBgNVBAcMB1V0cmVjaHQxFTATBgNVBAoMDFNVUkZuZXQgQi5WLjETMBEGA1UECwwKU1VSRmNvbmV4dDErMCkGA1UEAwwiZW5naW5lLnRlc3Quc3VyZmNvbmV4dC5ubCAyMDE4MDIwODCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANAJtsoE3s5adBMuO3BjV3mWaT4dLwgqHwyS/07Nnr/EwC4QlzryEwDXvxh/ZVSeyDa/VCOQZrx5hKcyUcoyCT+FCTfm5mF+90ROeyoIgMxK3S9vXPAwWugysUYEw2ZAV7xYSjZ/63rpFdJJ1dDgLdjOPsnEuYzrRIM9akBQlcg6xb4plRwRDwxkZvTEyD/xzEc3Xi62g6ag1cnhRubuxoGCdGUW+5U8WNyW4tY5NEN/t/pZPXqmEvAwlU3C5XZX0+aKbq1n73gsRv10nJzmDpwl/JYx73sgS6vrnIAdl942c9TnSiTxvL4SDtGP/mP2iq+q6ewZAPSkfEIl+5p4zAMCAwEAAaNdMFswHQYDVR0OBBYEFC7iwe/L6YQHDhtxYBdxBiIiaVnbMB8GA1UdIwQYMBaAFC7iwe/L6YQHDhtxYBdxBiIiaVnbMAwGA1UdEwQFMAMBAf8wCwYDVR0PBAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQC6MXBNfAPL5RSYuall2y0v2PjBigHD42zKC48h1Dp2K1zctTusPEStB1MfFTUA0dNYu+w10ablEtin8Nnk3UyNqOAqR55mNL0xDVnH/IG+iuGhmWmtv9DjI540hA9wR3bflzrpv4iBx3mlxpVO0+qvR+gwWZcDwC//g67TpGyRxFOZBS6g7FAnVJD0m72N68gQJ/zly8/ZfMjTrrLl5Gr3bqPJTG2JQazCXhE+2T9QRzdk+dyoTj0v9yrTlGkXFyOMn27Z0s5aW8iOrkJNClwSI5VO6i/g4p+g3aNVpcjzdRoX+YlC1fmoL9T66Uw2yVsmwRmQRmNghG8m27MuhRwO',
        ),
    ),
    'saml20.sign.assertion' => true,
);


$metadata['https://engine.test2.surfconext.nl/authentication/sp/metadata'] = [
    'entityid' => 'https://engine.test2.surfconext.nl/authentication/sp/metadata',
    'metadata-set' => 'saml20-sp-remote',
    'AssertionConsumerService' => [
        [
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
            'Location' => 'https://engine.test2.surfconext.nl/authentication/sp/consume-assertion',
            'index' => 0,
        ],
    ],
    'attributes.NameFormat' => 'urn:oasis:names:tc:SAML:2.0:attrname-format:uri',
    'keys' => [
        [
            'encryption' => false,
            'signing' => true,
            'type' => 'X509Certificate',
            'X509Certificate' => 'MIIDYDCCAkigAwIBAgIJANN/l9DYjIVPMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwHhcNMTgxMTI3MTQzMDU0WhcNMTkwMzA3MTQzMDU0WjBFMQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA+bVH25y9v+a+XK8FHKPLto2PnWbNTC/a5BlHLCoFL/JvycPuoDwgkYKaI4DLc50iMkrA7Grw10JVESdxeDANxlDUr9YS5HIRfGx6KCBGcKkvr+FK5Y3dxaEq27ADKNKxSl7e6wRg4pMwOvbw8JxUyWQcQZICNSwImSeQ2NOju+B5kE8CjS0uvBqpsXovuGeJUHvycdETYXnFpAdRKoOa3KxrnHjTP9o72QZGULBvPLu1X9KzwUli6YxRK2q8MawqMdLqONm+J022M/fa75tTicNTVoYfeRg7mITmrBw/0NT2uRtW3vClmmXh3JB3/BO/9z4v7gwhBX3tgBeBBDyZowIDAQABo1MwUTAdBgNVHQ4EFgQU9DLhS+n5J4Uw05wHlyAYk+YLSPowHwYDVR0jBBgwFoAU9DLhS+n5J4Uw05wHlyAYk+YLSPowDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAJt8KYOoJqgXTk01qGl6fc8nSNvreMNlIcc+sq71mYJ1GUlxx+vZ0Uf0NCnb3A4EQKMGh0A0eSTKjlLHHvHYVJOzrRziSu/RtAdA+2C809AG4YL7wtKg/JI2rBUI0ysZozFSNba6AnLq1K97LefC0pcniuBqV89SmMW2+So3v8yvrPzfKNXDAtR73nCkVLNuK5d8RZpOmgN4BHJ2VL34HYfMMwA/AE1JakWs8o5iu2+wlBrX0CQ/FFYxlcsLnFcv4K2+t/24IqGfNjymf3YizQ2Zs4h4dsg9Hn+HjxGR3bLOZGf3THFwP/A3VWH8tllxx9y9DKRm0eLJqg7MATah5Ag==',
        ],
    ],
    'saml20.sign.assertion' => true,
];

