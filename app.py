from flask import (
    Flask, )
from utils import (
    log, )

from config import config_
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.config.update(
        dict(
            DATABASE=os.path.join(app.root_path, 'db', 'splite.db'),
            SECRET_KEY='development key',
            USERNAME='admin',
            PASSWORD='default',
            SESSION_REFRESH_EACH_REQUEST=True,
        ))

    # init_app db init
    from models.__init__ import init_app
    init_app(app)

    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
    from routes.index import main as index_routes
    app.register_blueprint(index_routes)
    return app


# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config_.update(dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    ))
    app = create_app()
    app.run(**config_)
