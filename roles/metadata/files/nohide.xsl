<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
    xmlns:mdattr="urn:oasis:names:tc:SAML:metadata:attribute"
    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
    version="1.0">

    <xsl:output method="xml" indent="yes" omit-xml-declaration="no"/>

    <xsl:template match="md:EntitiesDescriptor">
        <xsl:copy>
            <xsl:copy-of select="*[
                not(md:Extensions/mdattr:EntityAttributes/saml:Attribute[@Name='http://macedir.org/entity-category']/saml:AttributeValue[text()='http://refeds.org/category/hide-from-discovery'])
                ]"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
