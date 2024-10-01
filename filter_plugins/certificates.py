# small filters to manupulate X509 certs
class FilterModule(object):

    # given a PEM-formatted certificate or private key, return the bare key
    # (without "-----END CERTIFICATE-----" etc)
    @staticmethod
    def _barepem(pem):
        str = pem
        # remove boilerplate
        for remove in ('-----BEGIN PRIVATE KEY-----', '-----END PRIVATE KEY-----',
                       '-----BEGIN CERTIFICATE-----', '-----END CERTIFICATE-----'):
            str = str.replace(remove, '')
        # get rid of empty lines etc (https://stackoverflow.com/questions/1140958)
        return "".join([s.strip() for s in str.splitlines() if s.strip(" \t\r\n")])

    def filters(self):
        return {
            'barepem': self._barepem
        }

