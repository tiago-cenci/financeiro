from flask import Flask
from config import Config
from models import db
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    return 'API Controle Financeiro OK ✅'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
