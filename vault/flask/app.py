from flask import Flask, render_template, request
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def home():
    print(request.method)
    if request.method == 'GET': print(request.args)
    return render_template('index.html')


# if __name__ == '__main__':
#     app.run(debug=True, port=5000)