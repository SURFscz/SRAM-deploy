<?php

/**
 * SAML 2.0 remote SP metadata for SimpleSAMLphp.
 *
 * See: https://simplesamlphp.org/docs/stable/simplesamlphp-reference-sp-remote
 */

$metadata['https://test-idp.sram.surf.nl/saml/module.php/saml/sp/metadata.php/default-sp'] = [
    'SingleLogoutService' => [
        [
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
            'Location' => 'https://test-idp.sram.surf.nl/saml/module.php/saml/sp/saml2-logout.php/default-sp',
        ],
    ],
    'AssertionConsumerService' => [
        [
            'index' => 0,
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
            'Location' => 'https://test-idp.sram.surf.nl/saml/module.php/saml/sp/saml2-acs.php/default-sp',
        ],
        [
            'index' => 1,
            'Binding' => 'urn:oasis:names:tc:SAML:1.0:profiles:browser-post',
            'Location' => 'https://test-idp.sram.surf.nl/saml/module.php/saml/sp/saml1-acs.php/default-sp',
        ],
        [
            'index' => 2,
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact',
            'Location' => 'https://test-idp.sram.surf.nl/saml/module.php/saml/sp/saml2-acs.php/default-sp',
        ],
        [
            'index' => 3,
            'Binding' => 'urn:oasis:names:tc:SAML:1.0:profiles:artifact-01',
            'Location' => 'https://test-idp.sram.surf.nl/saml/module.php/saml/sp/saml1-acs.php/default-sp/artifact',
        ],
    ],
];

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
                'sram-support@surf.nl',
            ],
        ],
        [
            'contactType' => 'administrative',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-support@surf.nl',
            ],
        ],
        [
            'contactType' => 'support',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-support@surf.nl',
            ],
        ],
        [
            'contactType' => 'other',
            'givenName' => 'Security Response Team',
            'emailAddress' => [
                'securityincident@surf.nl',
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
    'attributes' => [
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',
        'urn:oid:2.5.4.3',
        'urn:oid:2.16.840.1.113730.3.1.241',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.9',
        'urn:oid:2.5.4.4',
        'urn:oid:2.5.4.42',
        'urn:oid:0.9.2342.19200300.100.1.3',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.16',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.11',
        'urn:oid:1.3.6.1.4.1.25178.1.2.9',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.10',
    ],
    'attributes.required' => [
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',
        'urn:oid:2.5.4.3',
        'urn:oid:2.16.840.1.113730.3.1.241',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.9',
        'urn:oid:2.5.4.4',
        'urn:oid:2.5.4.42',
        'urn:oid:0.9.2342.19200300.100.1.3',
    ],
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
            'en' => 'https://wiki.surfnet.nl/display/SRAM/Privacy+Policy',
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

$metadata['https://proxy.sram.surf.nl/metadata/backend.xml'] = [
    'entityid' => 'https://proxy.sram.surf.nl/metadata/backend.xml',
    'description' => [],
    'OrganizationName' => [
        'en' => 'SURF',
    ],
    'name' => [
        'en' => 'SURF Research Access Management',
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
                'sram-support@surf.nl',
            ],
        ],
        [
            'contactType' => 'administrative',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-support@surf.nl',
            ],
        ],
        [
            'contactType' => 'support',
            'givenName' => 'SURF Research Access Management',
            'emailAddress' => [
                'sram-support@surf.nl',
            ],
        ],
        [
            'contactType' => 'other',
            'givenName' => 'Security Response Team',
            'emailAddress' => [
                'securityincident@surf.nl',
            ],
        ],
    ],
    'metadata-set' => 'saml20-sp-remote',
    'AssertionConsumerService' => [
        [
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST',
            'Location' => 'https://proxy.sram.surf.nl/saml2sp/acs/post',
            'index' => 1,
        ],
    ],
    'SingleLogoutService' => [],
    'NameIDFormat' => 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent',
    'attributes' => [
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',
        'urn:oid:2.5.4.3',
        'urn:oid:2.16.840.1.113730.3.1.241',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.9',
        'urn:oid:2.5.4.4',
        'urn:oid:2.5.4.42',
        'urn:oid:0.9.2342.19200300.100.1.3',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.16',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.11',
        'urn:oid:1.3.6.1.4.1.25178.1.2.9',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.10',
    ],
    'attributes.required' => [
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',
        'urn:oid:2.5.4.3',
        'urn:oid:2.16.840.1.113730.3.1.241',
        'urn:oid:1.3.6.1.4.1.5923.1.1.1.9',
        'urn:oid:2.5.4.4',
        'urn:oid:2.5.4.42',
        'urn:oid:0.9.2342.19200300.100.1.3',
    ],
    'attributes.NameFormat' => 'urn:oasis:names:tc:SAML:2.0:attrname-format:uri',
    'keys' => [
        [
            'encryption' => false,
            'signing' => true,
            'type' => 'X509Certificate',
            'X509Certificate' => 'MIIC1DCCAbwCCQDM9v704oVBezANBgkqhkiG9w0BAQsFADAsMSowKAYDVQQDDCFzdXJmX3JhbSBwcm9kIHByb3h5IHNhbWwyX2JhY2tlbmQwHhcNMjAwNTI4MTA1NDM2WhcNMzAwNTI2MTA1NDM2WjAsMSowKAYDVQQDDCFzdXJmX3JhbSBwcm9kIHByb3h5IHNhbWwyX2JhY2tlbmQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5Wcdmrn3L+wwfd/xs5IdEOQHp9VkhHTdgcVXt8SEH7YHBB4OauFOH8eQiQj543wKjLP06VV3MgD2cBTrSoOBSigCc/r8wNFPr9PP3XEeX3hXoQUTzKkbv7zOnQGf/8fRoAHSCUitdJkwXvi+wDkKr3qel8lVY0rl2kf1H/NSZkgwiPUsB8/VpThDL+55oH47dB3JrpfSNaduNElBIPVNtWZO64rqb/vHlLhkS9R6Ri6oKbJK0fP/HBcDMS/ngKAFRhxteaIdxQc9KosYejA/B/3tXRb5TqFCt6Uf7KU7mCR36VU/g6ii/IhB2uNrIhploeoj/abhjAaH29eqsQcSFAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAJ4YOT1YYN5E2s/lMJSp/tU2syGiVTPpJM5oA2nt+So+9KKotNpWKsCDCve1+4P+R6EN1wxcrjHModcZYmmJlq6Lh3YDcgki56FvvVwiV/dDTtzzj/stej9nM51UoLjeH8VvsgQ80cTV0kAIOl0JI1zuiivUMNXWvU8UKYsVrhqsz/lCfP5Ov5Lkw1RXOfJ4KkHjpyPvSAdeEYG5XmKD7ni5yURHaEkhQxqHo5C6lqkiy9aoO3hhzn3Weja4PS0UrZsrziz9cYa0U/XMO6SwzK6IjY0Q6bsXYmdK/+YCN+OEXPnujMfxsgFKHTVkYJ2OaYcl7BrvR9BqhVuQcI8i0vg=',
        ],
        [
            'encryption' => true,
            'signing' => false,
            'type' => 'X509Certificate',
            'X509Certificate' => 'MIIC1DCCAbwCCQDM9v704oVBezANBgkqhkiG9w0BAQsFADAsMSowKAYDVQQDDCFzdXJmX3JhbSBwcm9kIHByb3h5IHNhbWwyX2JhY2tlbmQwHhcNMjAwNTI4MTA1NDM2WhcNMzAwNTI2MTA1NDM2WjAsMSowKAYDVQQDDCFzdXJmX3JhbSBwcm9kIHByb3h5IHNhbWwyX2JhY2tlbmQwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5Wcdmrn3L+wwfd/xs5IdEOQHp9VkhHTdgcVXt8SEH7YHBB4OauFOH8eQiQj543wKjLP06VV3MgD2cBTrSoOBSigCc/r8wNFPr9PP3XEeX3hXoQUTzKkbv7zOnQGf/8fRoAHSCUitdJkwXvi+wDkKr3qel8lVY0rl2kf1H/NSZkgwiPUsB8/VpThDL+55oH47dB3JrpfSNaduNElBIPVNtWZO64rqb/vHlLhkS9R6Ri6oKbJK0fP/HBcDMS/ngKAFRhxteaIdxQc9KosYejA/B/3tXRb5TqFCt6Uf7KU7mCR36VU/g6ii/IhB2uNrIhploeoj/abhjAaH29eqsQcSFAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAJ4YOT1YYN5E2s/lMJSp/tU2syGiVTPpJM5oA2nt+So+9KKotNpWKsCDCve1+4P+R6EN1wxcrjHModcZYmmJlq6Lh3YDcgki56FvvVwiV/dDTtzzj/stej9nM51UoLjeH8VvsgQ80cTV0kAIOl0JI1zuiivUMNXWvU8UKYsVrhqsz/lCfP5Ov5Lkw1RXOfJ4KkHjpyPvSAdeEYG5XmKD7ni5yURHaEkhQxqHo5C6lqkiy9aoO3hhzn3Weja4PS0UrZsrziz9cYa0U/XMO6SwzK6IjY0Q6bsXYmdK/+YCN+OEXPnujMfxsgFKHTVkYJ2OaYcl7BrvR9BqhVuQcI8i0vg=',
        ],
    ],
    'validate.authnrequest' => false,
    'saml20.sign.assertion' => false,
    'UIInfo' => [
        'DisplayName' => [
            'en' => 'SURF Research Access Management',
        ],
        'Description' => [
            'en' => 'SURF Research Access Management',
        ],
        'InformationURL' => [
            'en' => 'https://www.surf.nl/en/surf-research-access-management-collaborating-easily-and-securely-in-research-services',
        ],
        'PrivacyStatementURL' => [
            'en' => 'https://wiki.surfnet.nl/display/SRAM/Privacy+Policy',
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
