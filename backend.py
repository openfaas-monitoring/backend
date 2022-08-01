from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# app的配置选项
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


@app.route('/', methods=['GET'])
def hello():
    temp = {"1": 2}
    return jsonify(temp)


if __name__ == '__main__':
    app.run()
