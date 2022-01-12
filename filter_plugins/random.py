import secrets


# hashing filters
class FilterModule(object):

    # generate a base64-encoded sha1 hash, as 'slappasswd -h {SHA}' gives
    @staticmethod
    def _rand_hex(number):
        num_bytes = int(number)
        if (num_bytes <= 0):
            return ""
        return secrets.token_hex(num_bytes)

    def filters(self):
        return {
            'random_hex': self._rand_hex
        }
