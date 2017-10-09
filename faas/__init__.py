from flask import Flask
from faas.api import v1

app = Flask(__name__)
app.register_blueprint(v1.mod)

