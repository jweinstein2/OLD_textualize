from flask import Flask, request
from flask_cors import CORS

import src.setup as setup
import src.analyze as analyze
import src.stats as stats

app = Flask(__name__)
CORS(app)

@app.route('/')
def _():
        return "Hello World!"

@app.route('/api/data/src/guess', methods = ['GET'])
def guess_src():
    return setup.guess_src()

@app.route('/api/data/src/', methods = ['GET'])
def api_get_src():
    return setup.get_src()

@app.route('/api/data/src/', methods = ['POST'])
def api_set_src():
    return setup.set_src(request.form['value'])

@app.route('/api/data/setup', methods = ['POST'])
def api_setup():
    return setup.preprocess()

@app.route('/api/data/process', methods = ['POST'])
def api_process():
    if analyze.process():
        return 'success'
    return 'failure'

@app.route('/api/convos', methods = ['GET'])
def api_contacts(n=15):
    return stats.contacts(n)

@app.route('/api/convos/summary', methods = ['GET'])
def api_summary():
    return stats.summary()

@app.route('/api/convos/frequency', methods = ['GET'])
@app.route('/api/convos/<number>/frequency', methods = ['GET'])
def api_frequency(number=None):
    return stats.frequency(number)

if __name__ == '__main__':
    app.run(debug=True)
