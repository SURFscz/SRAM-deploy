class FilterModule(object):

    # escape ldap-unsafe characters in a string
    @staticmethod
    def _ldap_escape(txt):
        for ch in (',', '\\', '#', '+', '<', '>', ';', '"', '='):
            txt = txt.replace(ch, '\\' + ch)
        return txt

    # escape %-characters in a string
    # (for use with python configparser, which treats % as interpolation strings)
    @staticmethod
    def _percent_escape(txt):
        txt = txt.replace('%', '%%')
        return txt

    def filters(self):
        return {
            'ldap_escape': self._ldap_escape,
            'percent_escape': self._percent_escape
        }
