from kubernetes import client, config


# 通过连接kubernetes来获取日志信息
class FunctionLogger:
    def __init__(self, config_path: str):
        self.k8s_client = config.new_client_from_config(config_path)
        self.api = client.CoreV1Api(api_client=self.k8s_client)
        self.func_map = self.getFuncAndPod()

    # 获取func_name和pod_name的对应关系
    def getFuncAndPod(self):
        pods = self.api.list_namespaced_pod(namespace='openfaas-fn').items
        func_map = dict()
        for pod in pods:
            pod_name = pod.metadata.name
            func_name = pod_name.split('-')[0]
            func_map[func_name] = pod_name
        return func_map

    # 获取函数的全部日志信息
    def getLogsFromFunction(self, func_name: str):
        res = {'status': 'success', 'logs': self.getLogsFromFunc1(func_name)}
        return res

    # 获取函数的运行信息
    def getFunctionRunningInfo(self, func_name: str):
        res = {'status': 'success', 'func_info': self.explainLogs(func_name=func_name)}
        return res

    # 获取since_seconds前的日志,如果不设置该参数，则表示查询所有的日志
    def getLogsFromFunc1(self, func_name: str, since_seconds=None):
        logs = self.api.read_namespaced_pod_log(name=self.func_map[func_name], namespace='openfaas-fn',
                                                since_seconds=since_seconds)
        return logs

    # 解析日志
    def explainLogs(self, func_name: str):
        res = dict()
        logs = self.getLogsFromFunc1(func_name=func_name, since_seconds=10)
        lines = logs.split('\n')
        begin_log = ''
        end_log = ''
        info_logs = list()
        for line in lines:
            if len(line) == 0:
                continue
            info = line.split(' ')
            if len(info) > 3:
                if info[2] == 'INFO':
                    info_logs.append(line)
                elif info[2] == 'Duration:':
                    end_log = line
                elif info[2] == 'Forking':
                    begin_log = line

        if len(end_log) > 0:
            res['status'] = 'end'
        elif len(begin_log) > 0:
            res['status'] = 'running'
        else:
            res['status'] = 'continue'

        res['invoke_info'] = FunctionLogger.explainRelation(info_logs)

        return res

    # 调用关系解析
    @staticmethod
    def explainRelation(info_logs):
        res = dict()
        for log in info_logs:
            info = log.split(' ')
            func_name, action = info[3], info[4]
            if func_name not in res.keys():
                res[func_name] = {
                    'status': '',
                    'invoke': []
                }
            if action == 'started':
                res[func_name]['status'] = 'started'
            if action == 'invoke':
                res[func_name]['invoke'].append(info[5])
        return res


if __name__ == '__main__':
    funcLogger = FunctionLogger('../resource/kubeconfig.yml')
    print(funcLogger.getFunctionRunningInfo('errlog'))
