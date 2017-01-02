# coding=utf-8
from flask import Flask
from config import config
from views import main, db
import os
import json

CONFIG_PATH = config['default'].SQLALCHEMY_DATABASE_URI[10:-7]
if not os.path.isdir(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

if not os.path.isfile(CONFIG_PATH + '/README'):
    DESCRIPTION = r'''该目录包括两个文件:

    tdl.json 是应用的选择配置文件，可修改 default 的值，默认的 default 为 development ，另外还可选择 production ;
    tdl.db 是应用的 SQLite 数据库文件。
    '''
    with open(CONFIG_PATH + '/README', 'w') as readme:
        readme.write(DESCRIPTION)

if not os.path.isfile(CONFIG_PATH + '/tdl.json'):
    config_str = {
        'default': 'default'
    }
    config_json = json.dumps(config_str)
    with open(CONFIG_PATH + '/tdl.json', 'w') as config_file:
        config_file.write(config_json)

app = Flask(__name__)
app.config.from_object(config['default'])
db.init_app(app)
app.register_blueprint(main)

if not os.path.isfile(config['default'].SQLALCHEMY_DATABASE_URI[10:]):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(port=9468)
