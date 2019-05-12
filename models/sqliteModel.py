"""
WHAT - 数据操作 model。
数据存储改为 sqlite。

HOW
"""
from utils import log, debug


class Model:
    __fields__ = [
        # (字段名, 类型, 值)
        # ('id', int, -1),
    ]

    # @classmethod
    # def new(cls, form=None, **kwargs):
    #     """用于外部的实例化方法."""
    #     m = cls()
    #     # 把定义的数据写入空对象, 未定义的数据输出错误
    #     fields = cls.__fields__.copy()
    #     if form is None:
    #         form = {}
    #
    #     for f in fields:
    #         k, t, v = f
    #         if k in form:
    #             setattr(m, k, t(form[k]))
    #         else:
    #             # 设置默认值
    #             setattr(m, k, v)
    #     # 处理额外的参数 kwargs
    #     for k, v in kwargs.items():
    #         if hasattr(m, k):
    #             setattr(m, k, v)
    #         else:
    #             raise KeyError
    #
    #     m.save()
    #     return m

    def setattr_with_form(self, form, **kwargs):
        # 把定义的数据写入空对象, 未定义的数据输出错误

        fields = self.__fields__.copy()
        if form is None:
            form = {}

        # 只从 form 中拿 fields 中预先设定数据.
        for f in fields:
            # key, type, value
            k, t, v = f
            if k in form:
                setattr(self, k, t(form[k]))
            else:
                # 设置默认值
                setattr(self, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise KeyError


def test():
    pass


if __name__ == '__main__':
    test()
