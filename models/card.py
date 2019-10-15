"""
WHAT - 定义  Card 类

HOW
"""
from models import (
    query_db,
    edit_db,
    today_text,
    review_days,
    execute,
    select_,
)
from models.model import (
    Base,
    Model,
)
from models.sqliteModel import Model as bModel
from utils import (
    log,
    debug
)
from sqlalchemy import (
    Column,
    MetaData,
    Table,
    Integer,
    String,
    text,
)


class Card(bModel):
    # for setattr
    __fields__ = bModel.__fields__ + [
        ('type', str, 'vocabulary'),
        ('front', str, -1),
        ('back', str, -1),
        ('in_plan', bool, 0),
    ]
    # for query
    __query__ = [
        'id',
        'type',
        'front',
        'back',
        'in_plan',
        'created',
    ]

    @classmethod
    def new(cls, form):
        """给外部使用的函数."""

        # 1. 更新实例的字段.
        c = cls()
        # 整理来自 form 的数据, 但是不包括 'created' 字段。
        # 这里去掉实例 c.__fields__ 中的 ‘created’，稍后自己设置.
        if ('created', str, '20010101') in c.__fields__:
            c.__fields__.remove(('created', str, '20010101'))
        c.setattr_with_form(form)
        # 更新 'created' 字段, 为当前实例创建的时间(str).
        setattr(c, 'created', today_text())

        # 2, 存入数据库中.
        c.insert()
        # 3, 返回插入数据的 id
        id_ = cls.query_max_id()
        log(f'验证查询到的最近插入记录的 id_ 是整数: {type(id_), id_}')
        return id_

    def insert(self):
        """从实例的字段, 执行数据库的插入动作."""
        # 1, 插入表 cards 中.
        sql_insert = '''
        INSERT INTO
            cards (type,front,back,in_plan,created)
        VALUES
            (?, ?, ?, ?, ?);
        '''
        args = (self.type, self.front, self.back, self.in_plan, self.created)
        r = edit_db(sql_insert, args)
        log(f'数据表 cards 插入一条 card.')

    @classmethod
    def query_max_id(cls):
        """通过查询 cards 中最大的 id, 来得到最近插入的那条记录的 id."""
        query = '''
        SELECT
            max(id)
        FROM
            cards
        '''
        r = query_db(query, one=True)
        log(f'查询 cards DB 最新记录的 id: {tuple(r), r.keys()}')
        if 'max(id)' in r.keys():
            return r['max(id)']
        else:
            return None

    @classmethod
    def all(cls):
        """显示所有的 card。

        返回的是 Sqlite3.Row 对象.
        """
        return cls.find_all()

    @classmethod
    def find_by(cls, **kwargs):
        query = '''
        SELECT
            *
        FROM
            cards
        WHERE
            [condition]
        ORDER BY id DESC
        '''
        # for k, v in kwargs.items():
        #     if k in cls.__fields__:

        # 'SELECT * FROM cards WHERE [contdition]' ->
        # 'SELECT * FROM cards WHERE type=? and created=?'
        cond, args = cls.format_kwargs(kwargs)
        sql = query.replace('[condition]', cond)
        return query_db(sql, args, one=False)

    @classmethod
    def find_one(cls, **kwargs):
        query = '''
        SELECT
            *
        FROM
            cards
        WHERE
            [condition];
        '''
        log(f'kwargs: {kwargs}')
        cond, args = cls.format_kwargs(kwargs)
        sql = query.replace('[condition]', cond)
        log(f'args: {args}')
        return query_db(sql, args, one=True)

    @classmethod
    def find_id_by(cls, **kwargs):
        query = '''
        SELECT
            id
        FROM
            cards
        WHERE
            [condition]
        '''
        # for k, v in kwargs.items():
        #     if k in cls.__fields__:

        # 'SELECT id FROM cards WHERE [contdition]' ->
        # 'SELECT id FROM cards WHERE type=? and created=?'
        cond, args = cls.format_kwargs(kwargs)
        sql = query.replace('[condition]', cond)
        _r = query_db(sql, args, one=False)
        if _r:
            _r = list(_r)
            _r = list(map(lambda i: i['id'], _r))
        return _r

    @classmethod
    def format_kwargs(cls, kwargs):
        # attrs cls.__fields__ 中预设的属性.
        attrs = [t for t in cls.__query__]
        # 拿到 attrs 中有的属性.
        cond_l = []
        val_l = []
        for k, v in kwargs.items():
            if k in attrs:
                cond_l.append(k + '=?')
                val_l.append(v)
        cond = ' and '.join(cond_l)
        args = tuple(val_l)
        # cond like 'type=? and created=?'.
        # args like ('vocabulary', '2019-5-4')
        # 返回 cond, args
        return cond, args

    @classmethod
    def find_id_by_ct(cls, ct):
        # return cls.find_all(created=ct)
        return cls.find_id_by(created=ct)

    @classmethod
    def find_by_ct(cls, ct):
        # return cls.find_all(created=ct)
        return cls.find_by(created=ct)

    @classmethod
    def find_all(cls):
        """
        数据查询
        """
        name = cls.__name__
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False

        # 构建 query 语句
        query = '''
        SELECT
            *
        FROM
            cards
        ORDER BY id DESC
        '''
        cs = query_db(query)
        if cs is None:
            cs = []
        l_ = [c for c in cs]
        return l_

    @classmethod
    def get_card_by_id(cls, card_id):
        log(card_id)
        return cls.find_one(id=card_id)


class Card(Base, Model):
    # 表的名字:
    __tablename__ = 'cards'

    # 表的结构:
    # 整数类型作为主键时, 默认是自增加的.
    id = Column(Integer, primary_key=True)
    type = Column(String(20), default='vocabulary')
    front = Column(String(20))
    back = Column(String(120))
    in_plan = Column(Integer, default=0)
    created = Column(String(12), default='2019-05-12')

    # 之前版本的 new 方法.
    # @classmethod
    # def new(cls, form):
    # """给外部使用的函数."""
    # 筛选出存在于 card 字段中的 k

    # type_ = form.get('type', 'vocabulary')
    # front_ = form.get('front', '')
    # back_ = form.get('back', '')
    # created_ = form.get('created', '')
    # cls(type=type_, front=front_, back=back_, created=created_)

    # 插入数据库中
    # cls.insert(d_)

    # 修改后的 new 方法.
    @classmethod
    def new(cls, form):
        """给外部使用的函数."""
        # 筛选出存在于表字段中的 k
        d_ = cls.filter_form(form)
        # d_增加 created 字段
        d_['created'] = today_text()
        # 插入数据库中
        debug(f'd_: {d_}')
        cls.insert(d_)

    @classmethod
    def find_id_by_ct(cls, ct):
        _table = cls.__table__
        r = select_(_table.select().where(cls.created == ct), one=True)
        return r.id

    # @classmethod
    # def get_card_by_id(cls, card_id):
    #     log(card_id)
    #     return cls.find_one(id=card_id)

    @classmethod
    def find_one(cls, **kwargs):
        log('find one by kwargs.')

        query = '''
        SELECT
            *
        FROM
            cards
        WHERE
            [condition];
        '''
        log(f'kwargs: {kwargs}')
        cond = cls.format_kwargs(kwargs)
        sql = query.replace('[condition]', cond)
        args = cls.filter_form(kwargs)
        log(f'args: {args}')
        return query_db(text(sql), args, one=True)

    @classmethod
    def format_kwargs(cls, kwargs):
        # attrs cls.__fields__ 中预设的属性.
        attrs = [t for t in cls.__query__]
        # 拿到 attrs 中有的属性.
        cond_l = []
        for k, v in kwargs.items():
            if k in attrs:
                cond_l.append(k + '=:' + k)
        cond = ' and '.join(cond_l)
        # cond like 'type=:type and created=:created'.
        # args like {'type': 'vocabulary', 'created': '2019-5-4'}
        # 返回 cond, args

        return cond


def test():
    form = {
        'type': 'vocabulary',
        'front': 'qeury',
        'back': '查询',
    }
    c = Card()
    setattr(c, 'type', 'vocabulary')
    log('Test ~', c.type)


if __name__ == '__main__':
    test()
