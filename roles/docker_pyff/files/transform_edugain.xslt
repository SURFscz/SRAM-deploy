<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
                xmlns:mdrpi="urn:oasis:names:tc:SAML:metadata:rpi"
                xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
                version="2.0">
    <!-- Cleanup -->
    <xsl:template match="@ID"/>
    <xsl:template match="@Id"/>
    <xsl:template match="@xml:id"/>
    <xsl:template match="@validUntil"/>
    <xsl:template match="@cacheDuration"/>
    <xsl:template match="@xml:base"/>
    <xsl:template match="ds:Signature"/>

    <!-- copy only entityies that have a md:IdPSSODescriptor -->
    <xsl:template match="md:EntityDescriptor[md:IDPSSODescriptor]">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <!-- remove all children of entitydescriptor that are not md:IDPSSODescriptor or md:Extensions or md:Organization or md:ContactPerson -->
    <xsl:template match="md:EntityDescriptor/*[not(self::md:IDPSSODescriptor or self::md:Extensions or self::md:Organization or self::md:ContactPerson)]"/>

    <!-- copy everything else -->
    <xsl:template match="node() | @*">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>


</xsl:stylesheet>
