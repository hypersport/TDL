from views import main
from flask import Flask
from config import config

app = Flask(__name__)
app.config.from_object(config['default'])
app.register_blueprint(main)
if __name__ == '__main__':
    app.run(port=9468)
