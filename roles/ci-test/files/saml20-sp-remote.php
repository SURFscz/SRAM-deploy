<?php

/**
 * SAML 2.0 remote SP metadata for SimpleSAMLphp.
 *
 * See: https://simplesamlphp.org/docs/stable/simplesamlphp-reference-sp-remote
 */
$metadata['https://proxy.acc.sram.eduteams.org/metadata/backend.xml'] = [
    'entityid' => 'https://proxy.acc.sram.eduteams.org/metadata/backend.xml',
    'description' => [],
    'OrganizationName' => [
        'en' => 'SURF',
    ],
    'name' => [
        'en' => 'SURF Research Access Management (Acceptance environment)',
    ],
    'OrganizationDisplayName' => [
        'en' => 'SURF',
    ],
    'url' => [
        'en' => 'https://www.surf.nl/',
    ],
    'OrganizationURL' => [
        'en' => 'https://www.surf.nl/',
    ],
    'contacts' => [
        [
            'contactType' => 'technical',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-beheer@surf.nl',
            ],
        ],
        [
            'contactType' => 'administrative',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-beheer@surf.nl',
            ],
        ],
        [
            'contactType' => 'support',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-beheer@surf.nl',
            ],
        ],
    ],
    'metadata-set' => 'saml20-sp-remote',
    'AssertionConsumerService' => [
        [
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
            'Location' => 'https://proxy.acc.sram.eduteams.org/saml2sp/acs/post',
            'index' => 1,
        ],
    ],
    'SingleLogoutService' => [],
    'NameIDFormat' => 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent',
    'attributes.NameFormat' => 'urn:oasis:names:tc:SAML:2.0:attrname-format:uri',
    'keys' => [
        [
            'encryption' => false,
            'signing' => true,
            'type' => 'X509Certificate',
            'X509Certificate' => 'MIIC4jCCAcoCCQC+LyygFrRKIjANBgkqhkiG9w0BAQsFADAzMTEwLwYDVQQDDChQcm94eSBzYW1sX3Byb3h5X2JhY2tlbmQgKHN1cmZuZXQtcGlsb3QpMB4XDTE5MDQwNTAyMDAzNVoXDTI5MDQwMjAyMDAzNVowMzExMC8GA1UEAwwoUHJveHkgc2FtbF9wcm94eV9iYWNrZW5kIChzdXJmbmV0LXBpbG90KTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKUDiv4jAiUYPd0UPOE9Kj2nkw4CEIrPblzpx9Bcem0KXHYy2iSSaMTiWpMiTdoy3WeN9Kr1IdLr2mcRAF2OM2NrTdiwkuUgJDwjBPAg9DxVPRoOn+UcGmcCVzHHIjS6pi4DOrKQoZa1PpPE52ZIaHfgQOsOQxoyXnnc1H161YmWSdTbCotuLkwuaAfUlgh/1ZsIW9MFy1prBAd/zTvXk5uLT2b05KQt3N5ZDoVDauIZFKqB4e5h4sbPagNxSCtahzHNCuuPFsyIzMxBf8348EzNABk0h022qmw4TcNqTd9PJhnBRemttLLV0kl/8SZU1ZV3uNCy6puJDvPqRB0J0FECAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAMZVNHu8C72bSaAhspfZjQIiG7A92eWsWW8F0A3l9p870kovXZpf8GAKmFERfYF/0lNfOkaSKkEqyOYNZQFx/VN0oDcpdCkgnGIhSt8K0sZ9MhZJkqYXrAfh3WFfjFpPdvQC33J9W3K481OORUzWeQTSd6sLmCpbdRatgbiwEvX4N2bHCGcFdIATwhIOqGA039UZundl4plIUo76EnqtGHvVaDrgztJINeuTVLtNq4yUR68nhNVSu94SpxknX/FgI6VfaY11fu71AFxLz4PFCvFlJ3/3JL9a4DZ55NsGu1AMv+jTKfG6ACW6uHE4tOa1DwJECVcf6a/9XEx4o2FgH4w==',
        ],
        [
            'encryption' => true,
            'signing' => false,
            'type' => 'X509Certificate',
            'X509Certificate' => 'MIIC4jCCAcoCCQC+LyygFrRKIjANBgkqhkiG9w0BAQsFADAzMTEwLwYDVQQDDChQcm94eSBzYW1sX3Byb3h5X2JhY2tlbmQgKHN1cmZuZXQtcGlsb3QpMB4XDTE5MDQwNTAyMDAzNVoXDTI5MDQwMjAyMDAzNVowMzExMC8GA1UEAwwoUHJveHkgc2FtbF9wcm94eV9iYWNrZW5kIChzdXJmbmV0LXBpbG90KTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKUDiv4jAiUYPd0UPOE9Kj2nkw4CEIrPblzpx9Bcem0KXHYy2iSSaMTiWpMiTdoy3WeN9Kr1IdLr2mcRAF2OM2NrTdiwkuUgJDwjBPAg9DxVPRoOn+UcGmcCVzHHIjS6pi4DOrKQoZa1PpPE52ZIaHfgQOsOQxoyXnnc1H161YmWSdTbCotuLkwuaAfUlgh/1ZsIW9MFy1prBAd/zTvXk5uLT2b05KQt3N5ZDoVDauIZFKqB4e5h4sbPagNxSCtahzHNCuuPFsyIzMxBf8348EzNABk0h022qmw4TcNqTd9PJhnBRemttLLV0kl/8SZU1ZV3uNCy6puJDvPqRB0J0FECAwEAATANBgkqhkiG9w0BAQsFAAOCAQEAMZVNHu8C72bSaAhspfZjQIiG7A92eWsWW8F0A3l9p870kovXZpf8GAKmFERfYF/0lNfOkaSKkEqyOYNZQFx/VN0oDcpdCkgnGIhSt8K0sZ9MhZJkqYXrAfh3WFfjFpPdvQC33J9W3K481OORUzWeQTSd6sLmCpbdRatgbiwEvX4N2bHCGcFdIATwhIOqGA039UZundl4plIUo76EnqtGHvVaDrgztJINeuTVLtNq4yUR68nhNVSu94SpxknX/FgI6VfaY11fu71AFxLz4PFCvFlJ3/3JL9a4DZ55NsGu1AMv+jTKfG6ACW6uHE4tOa1DwJECVcf6a/9XEx4o2FgH4w==',
        ],
    ],
    'validate.authnrequest' => false,
    'saml20.sign.assertion' => false,
    'UIInfo' => [
        'DisplayName' => [
            'en' => 'SURF Research Access Management (Acceptance environment)',
        ],
        'Description' => [
            'en' => 'SURF Research Access Management',
        ],
        'InformationURL' => [
            'en' => 'https://www.surf.nl/en/surf-research-access-management-collaborating-easily-and-securely-in-research-services',
        ],
        'PrivacyStatementURL' => [
            'en' => 'https://wiki.surfnet.nl/display/SRAM/SRAM+-+Privacy+Policy',
        ],
        'Logo' => [
            [
                'url' => 'https://static.surfconext.nl/logos/idp/surf.svg',
                'height' => 160,
                'width' => 200,
            ],
        ],
    ],
];

