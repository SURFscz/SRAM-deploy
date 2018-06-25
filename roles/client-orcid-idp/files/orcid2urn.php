<?php
$attributemap = array(
    // Attributes returned by ORCID
//     'orcid.uri'          => 'eduPersonOrcid', // URI with a 16-digit number
                                              // compatible with ISO 27729,
                                              // a.k.a. International Standard
                                              // Name Identifier (ISNI)
    'orcid.path'         => 'urn:mace:dir:attribute-def:uid', // The ORCID number formatted as
                                              // xxxx-xxxx-xxxx-xxxx
    'orcid.name'         => 'urn:mace:dir:attribute-def:displayName',
    'orcid.given-names'  => 'urn:mace:dir:attribute-def:givenName',
    'orcid.family-name'  => 'urn:mace:dir:attribute-def:sn',
    'orcid.email'        => 'urn:mace:dir:attribute-def:mail',
);