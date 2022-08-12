from kubernetes import client, config


# 通过连接kubernetes来获取日志信息
class FuncLogger:
    def __init__(self, config_path):
        self.k8s_client = config.new_client_from_config(config_path)
        self.api = client.CoreV1Api(api_client=self.k8s_client)
        self.func_map = self.getFuncAndPod()

    def getFuncAndPod(self):
        pods = self.api.list_namespaced_pod(namespace='openfaas-fn').items
        func_map = dict()
        for pod in pods:
            pod_name = pod.metadata.name
            func_name = pod_name.split('-')[0]
            func_map[func_name] = pod_name
        return func_map

    def getLogsFromFunc(self, func_name, since_seconds=10):
        logs = self.api.read_namespaced_pod_log(name=self.func_map[func_name], namespace='openfaas-fn',
                                                since_seconds=since_seconds)
        return logs


if __name__ == '__main__':
    funcLogger = FuncLogger('../resource/kubeconfig.yml')
    print(funcLogger.getLogsFromFunc('errlog'))
