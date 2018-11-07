import time

from cache import cache


def is_action_allowed(user_id, action_key, period, max_count):
    key = 'hist:%s:%s' % (user_id, action_key)
    now_ts = int(time.time() * 1000)
    with cache.pipeline() as pipe:
        pipe.zadd(key, now_ts, now_ts)
        pipe.zremrangebyscore(key, 0, now_ts - period * 1000)
        pipe.zcard(key)
        pipe.expire(key, period + 1)
        _, _, current_count, _ = pipe.execute()
    return current_count <= max_count
