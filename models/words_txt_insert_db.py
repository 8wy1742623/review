"""
WHAT - 读取 'data/words.txt', 录入数据库中.

HOW -
目的/问题定义:
    读取 'data/words.txt', 录入数据库中.
思路:
    1, 解释文件: foo3()
    2, 构造 card, Card.insert()
过程:
    1, 读取到 support, 及它下面的解释.
实现:
    ...
"""

from models import today_text
from models.card import Card


def foo3():
    with open('data/words.txt', encoding='utf-8') as f:
        lines = f.readlines()
        card_list = []
        card = []
        for l in lines:
            if '\n' != l:
                card.append(l)
            else:
                if card:
                    _c = [del_n(card.pop(0)), ''.join(card)]
                    card_list.append(_c)
                    card = []
    return card_list


def new_form(card_data):
    """构造form.

    form like:
    {'created': '2019-6-5',}
    """
    form = {
        'type': 'vocabulary',
        'front': card_data[0],
        'back': card_data[1],
        'in_plan': 1,
    }
    return form


def insert_from_txt():
    l = foo3()
    for i in l:
        Card.new(new_form(i))


def del_n(s):
    r = s.replace('\n', '')
    return r


def main():
    pass


if __name__ == '__main__':
    main()
