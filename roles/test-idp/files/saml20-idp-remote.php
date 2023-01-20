<?php

/**
 * SAML 2.0 remote IdP metadata for SimpleSAMLphp.
 *
 * Remember to remove the IdPs you don't use from this file.
 *
 * See: https://simplesamlphp.org/docs/stable/simplesamlphp-reference-idp-remote
 */

$metadata['https://test-idp.sram.surf.nl/saml/saml2/idp/metadata.php'] = [
    'metadata-set' => 'saml20-idp-remote',
    'entityid' => 'https://test-idp.sram.surf.nl/saml/saml2/idp/metadata.php',
    'SingleSignOnService' => [
        [
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
            'Location' => 'https://test-idp.sram.surf.nl/saml/saml2/idp/SSOService.php',
        ],
    ],
    'SingleLogoutService' => [
        [
            'Binding' => 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect',
            'Location' => 'https://test-idp.sram.surf.nl/saml/saml2/idp/SingleLogoutService.php',
        ],
    ],
    'certData' => 'MIIDEzCCAfugAwIBAgIURr0XJneuoPuyTDzs8kBYvQ5C9TEwDQYJKoZIhvcNAQELBQAwGDEWMBQGA1UEAwwNc2ltcGVsc2FtbHBocDAgFw0yMzAxMjAwOTI3MDlaGA8yMTIyMTIyNzA5MjcwOVowGDEWMBQGA1UEAwwNc2ltcGVsc2FtbHBocDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMLu9D6ohBx3mca2jLcR+ZfApTZTNmS+tclY2zURGaPQZFQPKVYC5B03H2UjIjJbKL9hOIzZqfCiTsZPEeDPnOSzt5MJ62CnBi1efWvWhg6XLYbPZ3d93GGuWMeTycBeL3KcBZxPhj5Mf4IsGFtgNTn73p5i312Z4czipkCuIuRvuI/TGw8GiC2Bi1xVyORjO/FGZdFtlQhO90szQ3wuXH1qnC5uZs3clcf0K8PVnIlyg4fdDYF2Hgk3WjP0eNVOk+cojfLdmRiQteD1QeHQBH5Q0vYuq+BBmhhZSTlcCTCAZCz8uTm/5eZHNqLiQ9lWe6CrWJK4li/7xzBvkXeWMdsCAwEAAaNTMFEwHQYDVR0OBBYEFLgajg10EEcOEVlzlXNVAC7MY1GDMB8GA1UdIwQYMBaAFLgajg10EEcOEVlzlXNVAC7MY1GDMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAExCh4PQh9ez4fYGWy0dXvvGCQ1CdHT3w/LPqU8sHZD3TJjrHdW4vbbC6TITYqAHaJqY9TNGE5Pxhw2pUHdBM87MZuxxrdktyJAxXSgWNd+XflH76amkN834o5ON6qhTOVrlCNI9N2HZRzSlnEsTUunTMT53DYcX2/iVUEm1Y3Bq/iyTteJvLGzEmL8jEYtySUvlU4NHNEmYkisVK/IaARMB66Afw9ykW9lF+QcJYxjpLa9XmCse4UDdkWNjIXIH8Winx7qLqsU1uKu+Thd6LIZg4Az+2hLSP5+CAnf6vo+ZkXdT6zNAMXOX50xoyW+RrtXMtzeidTAYIkFEhH7E9Xw=',
    'NameIDFormat' => 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient',
    'OrganizationName' => [
        'en' => 'SRAM Monitoring IdP',
        'nl' => 'SRAM Monitoring IdP',
    ],
    'OrganizationDisplayName' => [
        'en' => 'SRAM Monitoring IdP',
        'nl' => 'SRAM Monitoring IdP',
    ],
    'OrganizationURL' => [
        'en' => 'https://test-idp.sram.surf.nl/',
    ],
    'contacts' => [
        [
            'emailAddress' => 'sram-beheer@surf.nl',
            'contactType' => 'technical',
            'givenName' => 'Administrator',
        ],
    ],
];

