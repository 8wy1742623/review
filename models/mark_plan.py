from utils import (
    log,
    debug,
)
from models import (
    query_db,
    edit_db,
    today_text,
    review_days,
    execute,
    select_,
    review_days,
)
from models.model import (
    Base,
    Model,
)
from sqlalchemy import (
    Column,
    MetaData,
    Table,
    Integer,
    String,
    text,
)


class MarkPlan(Base, Model):
    # 表的名字:
    __tablename__ = 'mark_plan'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    ct = Column(String(12))
    # 使用该字段的目的: 记录这个表是否被标记过,
    # 但是实际使用过程中, 仅仅使用 ct 就够了.
    # 所有这个值, 有待修改.
    mark = Column(Integer, default=1)
    """操作 mark_plan 数据库"""

    def __init__(self):
        # 这个导致的问题，
        self.is_updated = False

    @classmethod
    def new(cls):
        """返回 MarkPlan 类的实例，

        实例的属性 is_updated， 表示是否需要更新 plan DB.

        1, 查询 mark_plan DB 标记的日期是否是今天.
        #暂时没有必要去查询这个 2, 查询今天是否添加了单词,
        """
        self = cls()

        ct_db = MarkPlan.query_ct()

        log(f'验证 ct_db 是表示时间的字符串: {ct_db}')
        if today_text() == ct_db:
            # 是当天,不需要更新;
            self.is_updated = False
        else:
            # 不是当天, 需要更新.
            MarkPlan.update_db()
            self.is_updated = True
        return self

    @classmethod
    def update_db(cls):
        log('to test.')
        ct_ = today_text()
        log(f'更新数据库 mark_plan: (id_, {ct_}, ).')
        d_ = {
            'ct': ct_
        }
        execute(cls.__table__.update(), d_)

    @classmethod
    def query_ct(cls):
        log('to test.')
        _table = cls.__table__
        place_ = _table.c.id == 1
        # r = select_(_table.select().where(place_).first(), one=True)
        r = select_(_table.select().where(place_), one=True)
        log(f'看查询结果 r: {r}')
        return r.ct
