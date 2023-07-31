from flask import Flask, render_template, request
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.dev.demo import Demo

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

conf = Demo.get_config_entries()

@app.route("/")
def home():
    params = {
        'filetype': request.args.filetype,
        'filepath': '/src/files',
        'csvdelimiter':  ','
    }

    dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **params)
    return render_template('index.html')


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)