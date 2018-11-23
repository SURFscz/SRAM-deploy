<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:mdattr="urn:oasis:names:tc:SAML:metadata:attribute"
    xmlns:mdrpi="urn:oasis:names:tc:SAML:metadata:rpi"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    version="1.0">

    <xsl:output method="xml" indent="yes" omit-xml-declaration="no"/>

    <xsl:template match="md:EntitiesDescriptor">
        <xsl:copy>
            <xsl:copy-of select="*[
                not(md:Extensions/mdrpi:RegistrationInfo[@registrationAuthority='http://www.surfconext.nl/'])
                ]"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
