# -*- coding: utf-8 -*-
from flask import Flask, current_app

import logging_config
from app import main_app
from app.auth import auth_app
from config import LOG
from services.app_session import RedisSessionInterface
from services.db_pool import DBPool

logging_config.config_logging(LOG.file_name, LOG.level)

app = Flask(__name__)
app.register_blueprint(main_app)
app.register_blueprint(auth_app)

app.app_context().push()
current_app.pool = DBPool()

app.session_interface = RedisSessionInterface(connection_pool=current_app.pool.redis_pool)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=False)
