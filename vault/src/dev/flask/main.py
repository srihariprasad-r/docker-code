# from flask import Flask, request, render_template
# import requests

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     otype = request.form.get('otype')
#     filetype = request.form.get('filetype')
#     try:
#         response = requests.get("http://127.0.0.1:5000/prepareobject", {
#         'otype': otype,
#         'filetype': filetype
#         })
#     except Exception as e:
#         print(e)
#     # print(response)
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host="127.0.0.1", port=5000, debug=True)