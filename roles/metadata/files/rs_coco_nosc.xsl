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
            <xsl:copy-of select="md:EntityDescriptor
            [md:Extensions/mdattr:EntityAttributes/saml:Attribute[starts-with(@Name,'http://macedir.org/entity-category')]/saml:AttributeValue[text()='http://www.geant.net/uri/dataprotection-code-of-conduct/v1']
            or md:Extensions/mdattr:EntityAttributes/saml:Attribute[starts-with(@Name,'http://macedir.org/entity-category')]/saml:AttributeValue[text()='http://refeds.org/category/research-and-scholarship']]
            [md:Extensions/mdrpi:RegistrationInfo[@registrationAuthority!='http://www.surfconext.nl/']]
            "/>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
