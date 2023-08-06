from flask import Flask, render_template, request, session
from flask_restful import Api, Resource
import os
import sys
import json
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
        session['params'] = {
            'filetype': filetype,
            'filepath': '/src/files',
            'csvdelimiter':  ','
            }
    else:
        session['otype'] = 'table'
        session['params'] = {
            'host': conf['DATABASE']['ADDRESS'], 
            'dbname': conf['DATABASE']['Database'],
            'table': conf['DATABASE']['TABLE']
            }

    dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **session['params'])
    if 'host' in session['params']: 
        res = ''
        db = DBClient(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'],**session['params'])
        conn = db.pgsql_connection(client = dbc.client)
        db.executeSQL(dbc.customer_table, conn)
        db.executeSQL(dbc.seed_customers, conn)
        cursor  = db.select_query(where_clause=' WHERE cust_no=1',conn=conn)
        for row in cursor:
            r = {}
            r['html'] = row[0]
        res += """<table align="left" border="1" cellpadding="3" cellspacing="3">\n<thead>\n"""
        res += "".join(["<th>"+cell+"</th>" for cell in dbc.customer_schema])
        res += "</thead>\n"
        res += "<tbody>\n"
        res += r['html']
        res += "</tbody>\n</table>\n<br>"
        return render_template('index.html', tbl_out=res)
    if 'filetype' in session['params']: 
        res = None
        fh = fileHandler(**session['params'])
        if filetype == 'csv':
            res = dbc.prepare_file(fh.filename, entries=dbc.csventries)
        if filetype == 'json':
            res = dbc.prepare_file(fh.filename)
            res = json.loads(res)
            return render_template('index.html', json_in=res)
        if filetype in ('parquet', 'avro'):
            res = dbc.prepare_file(fh.filename, entries=dbc.csventries)

        return render_template('index.html', out=res)

@app.route('/encrypt/', methods=['GET'])
def encryptfunc():
    api_args = request.args
    dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **session['params'])
    if 'host' in session['params']: 
        res = ''
        db = DBClient(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **session['params'])
        conn = db.pgsql_connection(client = dbc.client)
        rows = db.get_table_rows(conf=conf,table='customers', conn=conn)
        for row in rows:
            stmt = db.insert_statement(row, conf)
            db.executeSQL(stmt, conn)
        cursor = db.select_query(where_clause=' WHERE cust_no=2',conn=conn)
        for row in cursor:
            r = {}
            r['html'] = row[0]
        res += """<table align="left" border="1" cellpadding="3" cellspacing="3">\n<thead>\n"""
        res += "".join(["<th>"+cell+"</th>" for cell in dbc.customer_schema])
        res += "</thead>\n"
        res += "<tbody>\n"
        res += r['html']
        res += "</tbody>\n</table>\n<br>"
        return render_template('index.html', encr_tbl_out=res)
    else:
        if 'filetype' in session :
            encr_res = None
            flag = True
            encryptedlist = dbc.encryptfiles(conf)
            if session['filetype'] == 'csv':
                encr_res = dbc.prepare_file(dbc.targetencryptfilename, entries=encryptedlist)
            if session['filetype'] == 'json':
                encr_res = dbc.prepare_file(dbc.targetencryptfilename, entries=encryptedlist, flag = flag)
                return render_template('index.html', json_out=json.loads(encr_res))
            if session['filetype'] in ('parquet', 'avro'):
                encr_res = dbc.prepare_file(dbc.targetencryptfilename, df=encryptedlist)
                dbc.removefile(dbc.file_path, dbc.csvfile)

            return render_template('index.html', enc_out=encr_res)


if __name__ == '__main__':
    app.run(debug=True, port=5000)