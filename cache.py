import redis

cache = redis.StrictRedis()

cache.setnx('captcha_id', 0)
