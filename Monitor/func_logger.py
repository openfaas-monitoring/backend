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

    # 获取since_seconds前的日志,如果不设置该参数，则表示查询所有的日志
    def getLogsFromFunc1(self, func_name: str, since_seconds=None):
        logs = self.api.read_namespaced_pod_log(name=self.func_map[func_name], namespace='openfaas-fn',
                                                since_seconds=since_seconds)
        return logs

    # 获取函数的运行信息
    def getFunctionRunningInfo(self, func_name: str):
        res = {'status': 'success', 'func_info': "hahah"}
        return res


if __name__ == '__main__':
    funcLogger = FunctionLogger('../resource/kubeconfig.yml')
    print(funcLogger.getLogsFromFunction('ordertest'))
