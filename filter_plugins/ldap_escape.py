class FilterModule(object):

    # escape ldap-unsafe charactes in a string
    @staticmethod
    def _ldap_escape(txt):
        for ch in (',', '\\', '#', '+', '<', '>', ';', '"', '='):
            txt = txt.replace(ch, '\\' + ch)
        return txt

    def filters(self):
        return {
            'ldap_escape': self._ldap_escape
        }
