<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    version="1.0">

    <xsl:output method="xml" indent="yes" omit-xml-declaration="no"/>

    <xsl:template match="md:EntitiesDescriptor">
        <xsl:copy>
            <xsl:copy-of select="md:EntityDescriptor[md:SPSSODescriptor]"/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
