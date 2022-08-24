from Monitor.prometheus import PromQL, PrometheusCannotQuery
from Monitor.cadvisor import CAdvisor
from Monitor.kube_state_metrics import KubeState


# 对应openfaas-prometheus服务,监控函数级别的指标
class FunctionMonitor:
    def __init__(self, prom: PromQL, node_info):
        self.promQL = prom
        self.cadvisor = CAdvisor(prom)
        self.podsInfo = KubeState(prom).getPods()['pods']
        self.hostToInfo = node_info

    # 获取函数列表
    def getFunctions(self):
        res = {'status': 'error'}
        response = self.promQL.query('kube_pod_info{namespace="openfaas-fn"}')
        res['status'] = response['status']
        res['func'] = [record['metric']['pod'].split('-')[0] for record in response['data']]
        return res

    # 获取函数静态信息
    def getStaticInfoFromFunction(self, func: str):
        res = dict()
        try:
            res['image'] = self.getImagePos(func)
            res['replicas'] = self.getReplicas(func)
            res['invocations'] = self.getInvocationCount(func)
            res['running_api'] = self.getLogIP(func)

            res['status'] = 'success'
        except PrometheusCannotQuery:
            res['status'] = 'error'
        return res

    # 获取函数动态信息
    def getDynamicInfoFromFunction(self, func: str):
        res = self.cadvisor.getDynamicInfoFromPod(func)
        try:
            res['func_time'] = self.getFunctionTime(func)
            res['request_time'] = self.getRequestDuration(func)

            res['status'] = 'success'
        except PrometheusCannotQuery:
            res['status'] = 'error'
        return res

    # 函数对应镜像位置
    def getImagePos(self, func: str):
        query = 'kube_pod_container_info{{namespace="openfaas-fn", pod=~"^{func}.*"}}'.format(func=func + '-')
        return self.promQL.query(query)['data'][0]['metric']['image_spec']

    # 函数对应存储log的位置
    def getLogIP(self, func: str):
        for pod_info in self.podsInfo:
            if func == pod_info['pod_name']:
                return self.hostToInfo[pod_info['node']]
        return "No Match"

    # 函数副本数
    def getReplicas(self, func: str):
        query = 'gateway_service_count{{function_name="{func}.openfaas-fn"}}'.format(func=func)
        return int(self.promQL.query(query)['data'][0]['value'][-1])

    # 函数历史调用次数[成功和失败]
    def getInvocationCount(self, func: str):
        res = dict()
        query_success = 'gateway_function_invocation_total{{code="200",' \
                        'function_name="{func}.openfaas-fn"}}'.format(func=func)
        res['success'] = int(self.promQL.query(query_success)['data'][0]['value'][-1])
        query_error = 'gateway_function_invocation_total{{code!="200",' \
                      'function_name="{func}.openfaas-fn"}}'.format(func=func)
        response_error = self.promQL.query(query_error)['data']
        if len(response_error) == 0:
            res['error'] = 0
        else:
            res['error'] = int(response_error[0]['value'][-1])
        return res

    # 函数平均运行时间[ms]
    def getFunctionTime(self, func: str):
        query = 'gateway_functions_seconds_sum{{code="200",function_name="{func}.openfaas-fn"}} ' \
                '/ gateway_functions_seconds_count{{code="200",function_name="{func}.openfaas-fn"}}'.format(func=func)
        return float(self.promQL.query(query)['data'][0]['value'][-1]) * 1000

    # 函数平均响应时间[ms]
    def getRequestDuration(self, func: str):
        query = 'http_request_duration_seconds_sum' \
                '{{status="200", path="/system/function/{func}"}}' \
                '/ http_request_duration_seconds_count' \
                '{{status="200", path="/system/function/{func}"}}'.format(func=func)
        return float(self.promQL.query(query)['data'][0]['value'][-1]) * 1000


if __name__ == '__main__':
    promQL = PromQL('10.60.150.24:31119')
    functionMonitor = FunctionMonitor(promQL, {
        'vm-8c16g-node10': '10.60.150.24',
        'vm-2c4g-node6': '10.60.150.54',
        'vm-2c4g-node5': '10.60.150.55',
    })
    print(functionMonitor.getStaticInfoFromFunction('ordertest'))
