import os
import time
import uuid

from cache import cache as client
from captcha.image import ImageCaptcha


def is_action_allowed(user_id, action_key, period, max_count):
    key = 'hist:%s:%s' % (user_id, action_key)
    now_ts = int(time.time() * 1000)
    with client.pipeline() as pipe:
        pipe.zadd(key, now_ts, now_ts)
        pipe.zremrangebyscore(key, 0, now_ts - period * 1000)
        pipe.zcard(key)
        pipe.expire(key, period + 1)
        _, _, current_count, _ = pipe.execute()
    return current_count <= max_count


def create_captcha_image(captcha_id):
    image = ImageCaptcha()
    captcha = str(uuid.uuid4())[0:4]

    if not os.path.exists('captcha'):
        os.mkdir('captcha')
    file = 'captcha/captcha_{}.png'.format(captcha_id)
    image.write(captcha, file)
    return captcha.lower()
