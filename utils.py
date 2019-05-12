"""
需求：
1, 调用方式的改变 logger.debug -> debug.
    a, 也许不方便配置，退而求其次，
    l.debug()

    b, 也许使用统一配置：
    # 统一配置的情况属于，
    # 能够实现输出调用的所在函数， 所在行的情况下。
    # utils.py
    def log(*args, **kwargs):
        logger.info(*args, **kwargs)
    [] 要验证可行性。


2, 格式化：时间，
    参考：Formatting times using UTC (GMT) via configuration

3, 格式化：函数名字。
    参考：Logging to multiple destinations

4, 格式化：参数名：数值。
    参考：
    Using LoggerAdapters to impart contextual information

过程：
    [x] 1，字典配置 logger 。

    2，format
    [x] 2.1 时间
    [x] 2.2 函数/所在文件
    2.3 参数名：数值
"""

import logging
import logging.config
import os
import shutil

FILE_PATH = (r"D:\Program\AutoHotkey_1.1.29.01"
             r"\scripts\review_application\log.txt.log")


def owned_file_handler(filename, mode='a', encoding=None, owner=None):
    if owner:
        if not os.path.exists(filename):
            open(filename, 'a').close()
        shutil.chown(filename, *owner)
    return logging.FileHandler(filename, mode, encoding)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': ('%(asctime)s [%(levelname)s] %(module)s '
                       '%(filename)s %(funcName)s %(lineno)d - %(message)s'),
            'datefmt':
            '%b%d %H:%M',
        },
    },
    'handlers': {
        'file': {
            # The values below are popped from this dictionary and
            # used to create the handler, set the handler's level and
            # its formatter.
            '()': owned_file_handler,
            'level': 'DEBUG',
            'formatter': 'default',
            # The values below are passed to the handler creator callable
            # as keyword arguments.
            'filename': FILE_PATH,
            'mode': 'w',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('mylogger')
# logger.debug('A debug message')

# def deractor_log(func):
#     """改函数 logger.info 的默认参数。"""
#     def p():
#         func(msg=None, *args, **kwargs)
#     return p

# logger.info(msg=None)
# log = deractor_log(logger.info)

log = logger.info
debug = logger.debug


def test():
    a = 1
    log(f'a: {a}')


if __name__ == '__main__':
    test()
