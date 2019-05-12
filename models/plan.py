"""
WHAT

HOW

问题定义:
    提供给外界的方法(
        get_rand_card,
        get_card_by_id,
        get_today_plan,
    )
    需要的操作是:
    调用一个全局变量 Plan.
    这样可以缓存起来.
"""
from models import (
    query_db,
    edit_db,
    today_text,
    review_days,
)
from models.card import (
    Card, )
from utils import (
    log, )


def unpack(l):
    r = []
    for i in l:
        if isinstance(i, list):
            r = r + unpack(i)
        else:
            r.append(i)
    return r


class MarkPlan:
    """操作 mark_plan 数据库"""

    def __init__(self):
        """返回是否需要更新 plan DB.

        1, 查询 mark_plan DB 标记的日期是否是今天.
        2, 查询今天是否添加了单词,
        """
        ct_db = MarkPlan.query_ct()

        log(f'验证 ct_db 是表示时间的字符串: {ct_db}')
        if today_text() == ct_db:
            # 是当天,不需要更新;
            self.is_updated = False
        else:
            # 不是当天, 需要更新.
            MarkPlan.update_db()
            self.is_updated = True

    @staticmethod
    def update_db():
        query = '''
        UPDATE
            `mark_plan`
        SET
            `ct`=?
        WHERE
            `id`=?
        '''
        ct_ = today_text()
        id_ = 1
        edit_db(query, (
            ct_,
            id_,
        ))
        log(f'更新数据库 mark_plan: (id_, {ct_}, ).')

    @staticmethod
    def query_ct():
        query = '''
        SELECT
            ct
        FROM
            mark_plan
        WHERE
            id=?
        '''
        id_ = 1
        r = query_db(query, (id_, ), one=True)

        log(f'看查询结果 r: {r.keys()}, {tuple(r)}')

        if 'ct' in r.keys():
            ct = r['ct']
        else:
            ct = None
        return ct


class Plan:
    def __init__(self, need_update=False):
        log(f'Plan 的初始化是否需要更新数据库,' f'need_update: {need_update}')
        if need_update:
            Plan.update_db()

    @staticmethod
    def update_db():
        ids_in_plan = Plan._query_plans_id()
        log(f'验证 id_in_plan like [id(int)]: {ids_in_plan}')
        # 数据库操作:
        # 清空 plan
        Plan.init_plan_db()
        # 将 cards_in_plan 的每一个 id, 插入 plan 中.
        for i in ids_in_plan:
            log(f'验证 i like int: {i}')
            Plan.insert_id(i)
        log(f'Plan db update successfully.')

    @staticmethod
    def init_plan_db():
        log(f'验证是否出错.')
        query = '''DELETE FROM plans;'''
        edit_db(query)
        log(f'清空 plan db.')

    @staticmethod
    def insert_id(id_):
        sql_insert = '''
        INSERT INTO
            plans (card_id)
        VALUES
            (?);
        '''
        card_id = id_
        edit_db(sql_insert, (card_id, ))
        log(f'Insert plan db a record: (card_id={card_id},)')

    @staticmethod
    def _query_plans_id():
        """查找今日 plans 的过程.
        """
        # 生成日期字符串8个.
        today_t = today_text()
        ds = review_days(today_t)
        # 查询得到在这8个日期下, 创建的cards<sqlite3.Row>.
        cs = list(map(Card.find_id_by_ct, ds))
        cs = list(filter(lambda i: i, cs))  # 过滤下 cs 中的 None 子元素.
        # find_by_ct 返回的本身是 list, 于是 cs 是嵌套列表.
        cs = unpack(cs)
        # cs = list(map(lambda c: list(c), _cs))
        return cs

    @staticmethod
    def _query_plans():
        today_t = today_text()
        ds = review_days(today_t)
        # 查询得到在这8个日期下, 创建的cards<sqlite3.Row>.
        _cs = list(map(Card.find_by_ct, ds))
        _cs = list(filter(lambda i: i, _cs))  # 过滤下 cs 中的 None 子元素.
        # find_by_ct 返回的本身是 list, 于是 cs 是嵌套列表.
        cs = unpack(_cs)
        return cs

    def get_random_id(self):
        """ 查询数据库语句 - plan 中随机找一个 card_id 返回."""
        query = '''
        SELECT
            card_id
        FROM
            plans
        WHERE
            known = 0
        ORDER BY RANDOM()
        LIMIT 1
        '''
        r = query_db(query, one=True)
        # log(f'r: {r.keys()}')
        # r 可能值, 今天没有单词需要复习: None; 有的话,
        # 能找到, 是 <sqlite3.Row>.
        if r:
            if 'card_id' in r.keys():
                return r['card_id']
            else:
                return None
        else:
            return None

    def card_id_in_plan(self, card_id):
        """从 today_plan 中, 找到 id是 card_id 的 card."""
        # debug(f'self.today_plan: {self.today_plan[0].keys()}')
        select_sql = '''
        SELECT
            card_id
        FROM
            plans
        WHERE
            known=0 and card_id=?
        LIMIT 1
        '''
        r = query_db(select_sql, (card_id, ), one=True)
        log(f'查询结果: {r.keys()}')
        if 'card_id' in r.keys():
            log(f"{r['card_id']}, {card_id}")
            return int(card_id) == r['card_id']
        else:
            return False

    def set_known(self, c_id):
        update_sql = '''
        UPDATE
            `plans`
        SET
            `known`=?
        WHERE
            `card_id`=?
        '''
        query_db(update_sql, (1, c_id,), one=True)
        log(f'Update planDB ({c_id}, 0) -> ({c_id}, 1).')


def get_plan(date_text=None):
    """

    :param date_text: str
    :return: {Sqlite3.Row,}
    """
    mark_plan = MarkPlan()
    plan = Plan(mark_plan.is_updated)
    return plan._query_plans()


def get_rand_card():
    """返回随机 card 或 None."""
    # 实例化 mark_plan
    mark_plan = MarkPlan()
    # 实例化 plan
    plan = Plan(mark_plan.is_updated)
    c_id = plan.get_random_id()
    return Card.get_card_by_id(c_id)


def get_card_by_id(card_id):
    mark_plan = MarkPlan()
    plan = Plan(mark_plan.is_updated)
    log(f'验证 plan.card_id_in_plan(card_id) 的传入值 card_id - {card_id}')
    if plan.card_id_in_plan(card_id):
        card = Card.get_card_by_id(card_id)
        log(f'验证 card 类型, <sqlite3.Row> - {card}')
    else:
        card = None
        log(f'card_id 不在 plan 中.')
    return card


def set_known(c_id):
    mark_plan = MarkPlan()
    plan = Plan(mark_plan.is_updated)
    plan.set_known(c_id)


def main():
    pass


if __name__ == '__main__':
    main()
