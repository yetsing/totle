import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    formatted = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formatted, value)
    with open('club.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
