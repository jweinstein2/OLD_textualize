from flask_cors import CORS
from flask import Flask

from routes import *

app = Flask(__name__)
app.register_blueprint(routes, url_prefix='/api')
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
