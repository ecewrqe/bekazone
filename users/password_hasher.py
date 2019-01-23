#--coding:utf8--

from __future__ import absolute_import
from __future__ import unicode_literals

import random
import six
import hashlib

random.getstate()
def get_random_string(length=12, allow_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    return ''.join([random.choice(allow_chars) for i in range(length) ])

def compare_digest(val1, val2):
    '''
    比较两个字符串是否相等，
    1，长度是否相等
    2，内容是否相等
    如果内容相等，位^运算必定为0，必须每个对比都是0才是true，否则是或
    '''
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
    把字符串强行转换成bytes
    1，bytes:s必须传utf8格式的字节码
    2，可以传memoryview，直接转成bytes
    3，如果是字符串，自动转换{python2和python3的字符串格式判断}
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
    '''
    1, 生成hash
    2，比较hash
    encoding:传入字符串，salt随机生成盐
    verify:比较新的字符串和加密后的字符串
    :return: (格式:hash类型&hash值&盐)
    '''
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
        '''
        :param password:   要比较的加密前的密码
        :param encoded:    加密后的密码
        :return: 返回bool
        '''
        algorithm, hash, salt = encoded.split('&')
        encoded_2 = self.encoding(password, salt)
        return compare_digest(encoded, encoded_2)


class MD5PasswordHasher(object):
    '''
    不加盐md5hash
    encoding:传入字符串
    verify:比较新的字符串和加密后的字符串
    :return: (格式:hash类型&hash值&盐)
    '''
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
        '''
        :param password:   要比较的加密前的密码
        :param encoded:    加密后的密码
        :return: 返回bool
        '''
        hash = encoded
        encoded_2 = cls.encoding(password)
        return compare_digest(encoded, encoded_2)

