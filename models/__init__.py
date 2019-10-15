from flask import (current_app, g)
from datetime import (datetime, timedelta)
import sqlite3
from utils import log, debug


# def connect_db():
#     rv = sqlite3.connect(
#         current_app.config['DATABASE'],
#         detect_types=sqlite3.PARSE_DECLTYPES,
#     )
#     rv.row_factory = sqlite3.Row
#     log('connect splite.db')
#     return rv


# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     log('db operation.')
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db


def close_db(e=None):
    """Closes the database."""
    db = g.pop('sqlite_db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('data/schema.sql', mode='r') as f:
        db.executescript(f.read())
    db.commit()
    log('初始化数据库成功。')


def init_app(app):
    # fn'close_db' register with the app
    #
    # close_db function in the application factory,
    # so that it is called after each request.
    app.teardown_appcontext(close_db)


def query_db(query, args=(), one=False):
    """执行一条语句，并关闭连接。

    说明：该函数不包括 commit() 的执行，
    所以 query 语句的任何操作，都不会改变数据库。
    因此，这个函数仅设计为查询使用。
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    # cur.close()

    # return:
    if rv:
        if one:
            return rv[0]  # 返回找到的第一个
        else:
            return rv  # 返回所有找到的
    else:
        return None  # 没找到


def edit_db(sql_insert, args=()):
    conn = get_db()
    cur = conn.execute(sql_insert, args)
    rv = cur.fetchall()
    conn.commit()
    return rv


# 日期处理
def str_2_tm(tm_str: str) -> datetime:
    return parse_ymd(tm_str)


def tm_2_str(tm: datetime) -> str:
    """:return like '2019-05-01'."""
    fmt = '%Y-%m-%d'
    return tm.strftime(fmt)


def parse_ymd(s: str):
    """s like '2019-05-01'"""
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))


def today_text() -> str:
    td = datetime.today()
    return tm_2_str(td)


def review_days(review_date: str) -> {str}:
    """这天应该复习过去哪几天的学习的知识点.
    由复习日期, 得到复习内容的创建日期.
    """
    # '2019-5-4' -> datetime 实例 rv.
    rv = str_2_tm(review_date)
    # 当天, 1天前, 4天前, ...
    d_l = [0, 1, 4, 7, 15, 30, 90, 180]
    # 创建日期的 datetime 类型.
    ct_l = map(lambda d: substrac_days(rv, d), d_l)
    # 创建日期的 str 类型.
    ct_texts = map(lambda ct: tm_2_str(ct), ct_l)
    # todo return map -> list, or not.
    return ct_texts


def substrac_days(dt: datetime, days: int) -> datetime:
    return dt - timedelta(days)


import logging
from sqlalchemy import (
    Column,
    String,
    Integer,
    create_engine,
    ForeignKey,
    MetaData,
    Table,
    or_,
    and_,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
)
from sqlalchemy.sql.expression import text

def init_db():
    """使用 schema.sql 初始化db"""
    log('初始化数据库...')
    db = get_db()

    with current_app.open_resource('data/schema.sql', mode='r') as f:
        db.execute(text(f.read()))
    db.commit()
    log('初始化数据库成功.')


def init_app(app):
    # fn'close_db' register with the app
    #
    # close_db function in the application factory,
    # so that it is called after each request.
    app.teardown_appcontext(close_db)


def connect_db():
    logging.info('create database connection pool...')
    # 连接
    engine = create_engine('sqlite:///web8.sqlite', echo=False)

    meta = MetaData()
    meta.create_all(engine)

    # 创建 DBSession 类型:
    db_session = sessionmaker(bind=engine)
    log(f'db_session 类型: {type(db_session)}')

    return db_session


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        sess = connect_db()
        g.db = sess()
    return g.db


def close_db(e=None):
    """Closes the database."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def select_(sql, args=dict(), one=False):
    """执行一条语句，并关闭连接。

    说明：该函数不包括 commit() 的执行，
    所以 query 语句的任何操作，都不会改变数据库。
    因此，这个函数仅设计为查询使用。

    sql, args like:
    user_table.select().where(user_table.c.id == 5)

    "SELECT * FROM user WHERE id=:param",
    {"param":5}
    """
    log(f'SELECT 参数: {sql}, {args}')
    cur = get_db().execute(sql, args)
    rv = cur.fetchall()
    # cur.close()

    # return:
    if rv:
        if one:
            return rv[0]  # 返回找到的第一个
        else:
            return rv  # 返回所有找到的
    else:
        return None  # 没找到


def execute(sql, args=dict()):
    log(f'execute 参数: {sql}, {args}')
    sess = get_db()
    log(f'sess 类型: {type(sess)}')
    cur = sess.execute(sql, args)
    return postfix(cur)


def postfix(cur):
    rv = cur.fetchall()
    sess.commit()
    return rv

def unpack(l):
    r = []
    for i in l:
        if isinstance(i, list):
            r = r + unpack(i)
        else:
            r.append(i)
    return r

def review_days(review_days_text: str) -> {str}:
    pass

def test():
    # Test tm_2_str()
    # tm = str_2_tm('2019-5-6')
    # log(tm_2_str(tm))  # '2019-5-6'

    # Test parse_ymd()
    # log(parse_ymd('2019-01-03'))

    # Test today_text()
    log(today_text())


if __name__ == '__main__':
    test()
