"""
WHAT - orm and Model
"""
from models import (
    query_db,
    edit_db,
    today_text,
    review_days,
    execute,
    select_,
)
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
from utils import (
    log,
    debug
)

# 创建对象的基类:
Base = declarative_base()


class Model():

    @classmethod
    def insert(cls, form):
        # execute(cls.__table__.insert(), form)
        # 好像, 因为 id 没有给, 会导致 sql 执行错误.
        execute(cls.__table__.insert().values(form))

    def __repr__(self):
        d_ = {
            k: v
            for k, v in self.__dict__.items() if k != '_sa_instance_state'
        }

        s_ = self.create_args_string(d_)
        name = self.__class__.__name__
        return f"<{name}({s_})>"

    @staticmethod
    def create_args_string(d):
        L = []
        for k, v in d.items():
            s_ = str(k) + "='" + str(v) + "'"
            L.append(s_)
        return ', '.join(L)

    @classmethod
    def get_cols_name(cls):
        cols = cls.__table__.columns
        return [c.name for c in cols]

    @classmethod
    def filter_form(cls, form):
        cols_name = cls.get_cols_name()
        d_ = {
            k: v
            for k, v in form.items() if k in cols_name
        }
        return d_
