"""
WHAT - model

HOW - xxx
"""
import os

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from models.__init__ import init_db
from models.card import Card
from models.plan import (
    get_rand_card,
    get_plan,
    get_card_by_id,
    set_known,
    Plan
)
from models.words_txt_insert_db import insert_from_txt
from utils import (
    log,
    debug,
)

main = Blueprint('index', __name__)
"""
用户在这里可以
    首页
"""


# Uncomment and use this to initialize database, then comment it
# You can rerun it to pave the database and start over
@main.route('/init_db')
def init_database():
    init_db()
    return 'Initialized the database.'


@main.route("/")
def index():
    # todo user
    # if session.get('logged_in'):
    #     return render_template("index.html")
    # else:
    #     return redirect(url_for('login'))
    # log('GET /.')
    return render_template("index.html")


@main.route("/new")
def new_card():
    log('GET /new.')
    return render_template("add_card.html")


@main.route("/add", methods=['POST'])
def add_card():
    form = request.form
    # todo 用户判断
    # u = current_user()
    log(f'Card.__fields__: {Card.__fields__}')
    card_id = Card.new(form)
    plan = Plan()
    plan.insert_id(card_id)
    return redirect(url_for('.review', card_id=card_id))


@main.route("/cards")
def list_cards():
    cs = Card.all()
    # for test
    # cs 是什么
    # c = cs[0]
    # log(f'c: {c.keys()}')
    # log(f'c: {type(c)}')
    if not cs:
        flash('没有一张卡片。')
    return render_template('list_cards.html', cs=cs)


@main.route("/list_today_cards")
def list_today_cards():
    cs = get_plan()
    if not cs:
        flash('没有一张卡片。')
    return render_template('list_cards.html', cs=cs)


@main.route("/review")
@main.route("/review/<card_id>")
def review(card_id=None):
    log(f'card_id: {type(card_id)}')
    return memorize(card_id)

    # plans = Plan.today_plan()
    # if [[]] == plans:
    #     flash('今天没有复习内容。')
    # return render_template('review.html', plans=plans)


def memorize(card_id):
    if card_id:
        # todo 验证run[]
        card = get_card_by_id(card_id)
        log(f'看看 {card_id} 能否找到对应的 {card}')
        if not card:
            card = get_rand_card()
    else:
        # todo 验证run[].
        card = get_rand_card()

    if not card:
        # run[x]
        flash("You've learned all cards.")
        return redirect(url_for('.list_today_cards'))
    # todo run[]
    # debug(f'card: {card}')
    return render_template('review.html', card=card)


@main.route("/txt_insert_card")
def txt_insert_card():
    insert_from_txt()
    flash('插入成功.')
    return redirect(url_for('.index'))


@main.route('/mark_known/<card_id>')
def mark_known(card_id):
    log('观察变化: ')
    log(f"card_id: {card_id}")
    set_known(card_id)
    flash(f"Set card_id-{card_id} known.")
    # log(session['unknown'])
    # session['unknown'] = [11, 12]
    # session['unknown'].remove(11)
    # log(session['unknown'])
    return redirect(url_for('.review'))


@main.route("/test")
def test():
    return render_template('test.html')
