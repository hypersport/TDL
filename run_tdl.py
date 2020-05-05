from flask import Flask
from config import config
from views import main, db, login_manager, bootstrap
import os
import json

CONFIG_PATH = config['default'].SQLALCHEMY_DATABASE_URI[10:-7]
if not os.path.isdir(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

if not os.path.isfile(CONFIG_PATH + '/README'):
    DESCRIPTION = r'''第一次启动应用时会创建 $HOME/.tdl/ 目录，该目录包括三个文件:
- README 是说明文件
- tdl.json 是应用的选择配置文件
    ```
    {
    "config_type": "default",
    "host": "localhost",
    "port": 9468
    }
    ```
    - 修改 config_type 的值，默认的 default 为 development ，还可选择 production ;
    - 修改 host 的值;
    - 修改端口 port 的值
- tdl.db 是应用的 SQLite 数据库文件。
    '''
    with open(CONFIG_PATH + '/README', 'w') as readme:
        readme.write(DESCRIPTION)

if not os.path.isfile(CONFIG_PATH + '/tdl.json'):
    config_str = {
        'config_type': 'default',
        'host': 'localhost',
        'port': 9468
    }
    config_json = json.dumps(config_str)
    with open(CONFIG_PATH + '/tdl.json', 'w') as config_file:
        config_file.write(config_json)
    config_type = 'default'
    host = 'localhost'
    port = 9468
else:
    with open(CONFIG_PATH + '/tdl.json', 'r') as config_file:
        config_str = config_file.read()
    config_str = json.loads(config_str)
    config_type = config_str['config_type']
    host = config_str['host']
    port = config_str['port']

app = Flask(__name__)
app.config.from_object(config[config_type])
bootstrap.init_app(app)
db.init_app(app)
login_manager.init_app(app)
app.register_blueprint(main)

if not os.path.isfile(config['default'].SQLALCHEMY_DATABASE_URI[10:]):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(host=host, port=port)
