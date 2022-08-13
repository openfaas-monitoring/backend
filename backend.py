from flask import Flask, request, jsonify
from flask_cors import CORS
from Monitor.monitor import Monitor

app = Flask(__name__)
CORS(app)
# app的配置选项
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

# 全局监控对象[使用前需要先进行setIP]
monitor = Monitor()
monitor.setIP('10.60.150.24:31119')  # 测试使用


@app.route('/', methods=['GET'])
def hello():
    return 'hello world'


@app.route('/setIP', methods=['GET'])
def setIP():
    ip = request.args.get('ip')
    valid = monitor.setIP(ip)
    if valid:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'})


@app.route('/global/functions', methods=['GET'])
def getFunctions():
    return jsonify(monitor.getFunctions())


@app.route('/static/function', methods=['GET'])
def getStaticInfoFromFunction():
    func = request.args.get('func')
    return jsonify(monitor.getStaticInfoFromFunction(func))


@app.route('/dynamic/function', methods=['GET'])
def getDynamicInfoFromFunction():
    func = request.args.get('func')
    return jsonify(monitor.getDynamicInfoFromFunction(func))


@app.route('/global/pods', methods=['GET'])
def getPods():
    return jsonify(monitor.getPods())


@app.route('/static/pod', methods=['GET'])
def getStaticInfoFromPod():
    pod = request.args.get('pod')
    return jsonify(monitor.getStaticInfoFromPod(pod))


@app.route('/dynamic/pod', methods=['GET'])
def getDynamicInfoFromPod():
    pod = request.args.get('pod')
    return jsonify(monitor.getDynamicInfoFromPod(pod))


@app.route('/global/nodes', methods=['GET'])
def getNodes():
    return jsonify(monitor.getNodes())


@app.route('/dynamic/getPodsFromNode', methods=['GET'])
def getPodsFromNode():
    node = request.args.get('node')
    return jsonify(monitor.getPodsFromNode(node))


@app.route('/dynamic/node', methods=['GET'])
def getDynamicInfoFromNode():
    node = request.args.get('node')
    return jsonify(monitor.getDynamicInfoFromNode(node))


@app.route('/logs', methods=['GET'])
def getLogsFromFunction():
    func = request.args.get('func')
    return jsonify(monitor.getLogsFromFunction(func))


@app.route('/running', methods=['GET'])
def getRunningInfoFromFunction():
    func = request.args.get('func')
    return jsonify(monitor.getRunningInfoFromFunction(func))


if __name__ == '__main__':
    app.run()
