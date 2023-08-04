from flask import Flask, render_template, request, session
from flask_restful import Api, Resource
import os
import sys
from datetime import timedelta
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from demo import Demo
from fileHandler import fileHandler
from dbc import DBClient

template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./static')
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=5)
api = Api(app)

conf = Demo.get_config_entries()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/otype/')
@app.route('/otype/<filetype>', methods=['GET','POST'])
def prepare(filetype=None):
    api_args = request.args
    if filetype:
        session['otype'] = 'file'
        session['filetype'] = filetype
        params = {
            'filetype': filetype,
            'filepath': '/src/files',
            'csvdelimiter':  ','
        }
    else:
        session['otype'] = 'table'
        params = {
            'host': conf['DATABASE']['ADDRESS'], 
            'dbname': conf['DATABASE']['Database'],
            'table': conf['DATABASE']['TABLE']
        }

    if 'host' in params: db = DBClient(**params)
    dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **params)
    res = None
    if 'filetype' in params: 
        fh = fileHandler(**params)
        res = dbc.prepare_file(fh.filename, entries=dbc.csventries)

    return render_template('index.html', out=res)

@app.route('/encrypt/', methods=['GET'])
def encryptfunc():
    api_args = request.args
    if 'filetype' in session:
        params = {
            'filetype': session['filetype'],
            'filepath': '/src/files',
            'csvdelimiter':  ','
        }
    else:
        params = {
            'host': conf['DATABASE']['ADDRESS'], 
            'dbname': conf['DATABASE']['Database'],
            'table': conf['DATABASE']['TABLE']
        }

    if 'host' in params: db = DBClient(**params)
    dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **params)
    encr_res = None
    if 'filetype' in session and session['filetype'] == 'csv':
        encryptedlist = dbc.encryptfiles(conf)
        encr_res = dbc.prepare_file(dbc.targetencryptfilename, entries=encryptedlist)

    return render_template('index.html', enc_out=encr_res)


if __name__ == '__main__':
    app.run(debug=True, port=5000)