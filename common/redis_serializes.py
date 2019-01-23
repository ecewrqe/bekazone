# --coding:utf8--
from __future__ import unicode_literals
import redis
class RedisIO(object):
    def __init__(self, url):
        """
        统一使用url登陆
        :param url: redis://[password]@10.0.0.7:xxxx/[database]
        """
        self.rd01 = redis.from_url(url)

class TokenRedisIO(RedisIO):
    def redis_input_ex(self, name, value, expire=None):
        self.rd01.set(name, value, ex=expire)

    def redis_output(self, name):
        value = self.rd01.get(name)
        return value

    def redis_input_dict(self, name, key, value, expire):
        self.rd01.hset(name, key, value, expire)
    def redis_delete_name(self, name):
        self.rd01.delete(name)
    def has_name(self, name):
        keys_list = self.rd01.keys(name)
        if keys_list:
            return True
        else:
            return False

if __name__ == "__main__":
    trio = TokenRedisIO("redis://@localhost:6379/0")
    trio.redis_input_ex("ww", "bb",100)
    print(trio.redis_output("ww"))