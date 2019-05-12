from flask import (
    current_app,
    g
)
from datetime import (
    datetime,
    timedelta
)
import sqlite3
from utils import log, debug


def connect_db():
    rv = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    rv.row_factory = sqlite3.Row
    log('connect splite.db')
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


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
    return ct_texts


def substrac_days(dt: datetime, days: int) -> datetime:
    return dt - timedelta(days)


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
