import hashlib
import base64
import random


# hashing filters
class FilterModule(object):

    # generate a base64-encoded sha1 hash, as 'slappasswd -h {SHA}' gives
    @staticmethod
    def _sha1_b64(str) -> str:
        m = hashlib.sha1()
        m.update(str.encode('ASCII'))
        hash_bin = m.digest()
        hash_b64 = base64.b64encode(hash_bin)
        return hash_b64.decode('ASCII')

    # generate a MySQL-type password hash
    # see https://unix.stackexchange.com/questions/44883/encrypt-a-password-the-same-way-mysql-does
    @staticmethod
    def _sha1_mysql(str) -> str:
        str2 = str.encode('ASCII')
        res = hashlib.sha1(hashlib.sha1(str2).digest()).hexdigest()
        return '*' + res.upper()

    @staticmethod
    def _bcrypt_stable(secret: str, seed: str, rounds: int = 12, ident: str = "2b") -> str:
        # standard ansible.builtins.bcrypt generates a random salt, so is not idempotent
        # this is a workaround which generates a hash based on a given input string
        from passlib.hash import bcrypt

        # base set of chars to use for
        chars_allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        # choose 21 random chars from the set (see https://docs.python.org/3/library/secrets.html#module-secrets)
        random.seed(seed)
        salt = "".join(random.choices(chars_allowed, k=21))
        # final char should be one of [.Oeu] (see
        # https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html#format-algorithm)
        salt += random.choice('.Oeu')

        return bcrypt.using(rounds=rounds, ident=ident, salt=salt).hash(secret)

    def filters(self):
        return {
            'sha1_b64':   self._sha1_b64,
            'slapd_hash': lambda a: '{SHA}' + self._sha1_b64(a),
            'mysql_hash': self._sha1_mysql,
            'bcrypt_hash': self._bcrypt_stable,
        }
