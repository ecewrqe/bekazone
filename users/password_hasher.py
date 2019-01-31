import random
import six
import hashlib

random.getstate()
def get_random_string(length=12, allow_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    return ''.join([random.choice(allow_chars) for i in range(length) ])

def compare_digest(val1, val2):
    """
    compare two value
    """
    if len(val1) != len(val2):
        return False
    result=0
    if six.PY3 and isinstance(val1, bytes) and isinstance(val2, bytes):
        for x, y in zip(val1,val2):
            result |= x ^ y
    else:
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)
    return result == 0



def force_bytes(s, encoding='utf8', errors='strick'):
    '''
    force to change text encoding
    '''
    if isinstance(s, bytes):
        if encoding == 'utf8':
            return s
        else:
            s.decode("utf8", errors).encode(encoding, errors)
    elif isinstance(s, memoryview):
        bytes(s)
    elif isinstance(s, six.string_types):
        return s.encode(encoding, errors)
    else:
        s=six.text_type(s).encode(encoding, errors)
        return s



class SaltMD5PasswordHasher(object):
    algorithm = 'md5'
    def salt(self):

        return get_random_string()
    def encoding(self, password, salt=''):
        '''
        pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
        :param s:
        :return:
        '''
        assert password
        if salt == '':
            salt = self.salt()

        hash = hashlib.md5(force_bytes(password + salt)).hexdigest()
        return '%s&%s&%s' % (self.algorithm, hash, salt)

    def verify(self, password, encoded):
        algorithm, hash, salt = encoded.split('&')
        encoded_2 = self.encoding(password, salt)
        return compare_digest(encoded, encoded_2)


class MD5PasswordHasher(object):
    
    algorithm = 'md5'
    @staticmethod
    def encoding(password):
        '''
        pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
        :param s:
        :return:
        '''
        assert password

        hash = hashlib.md5(force_bytes(password)).hexdigest()
        return '%s' % (hash)

    @classmethod
    def verify(cls, password, encoded):
        
        hash = encoded
        encoded_2 = cls.encoding(password)
        return compare_digest(encoded, encoded_2)

