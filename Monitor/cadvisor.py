from Monitor.prometheus import PromQL, PrometheusCannotQuery
import time


# 对应cadvisor服务,监控容器级别的指标
class CAdvisor:
    def __init__(self, prom: PromQL):
        self.promQL = prom

    # pod相关静态信息查询
    def getStaticInfoFromPod(self, pod: str):
        res = dict()
        try:
            res['node'] = self.getNodeFromPod(pod)

            res['status'] = 'success'
        except PrometheusCannotQuery:
            res['status'] = 'error'
        return res

    # pod相关动态信息查询
    def getDynamicInfoFromPod(self, pod: str):
        end = time.time()
        res = dict()
        try:
            res['cpuRate'] = self.getCPURate(pod, end)
            res['memRate'] = self.getMemRate(pod, end)

            res['status'] = 'success'
        except PrometheusCannotQuery:
            res['status'] = 'error'

        return res

    # pod的CPU占用率随时间变化
    def getCPURate(self, pod: str, end: float):
        query = 'sum by(pod)(irate(container_cpu_usage_seconds_total{{pod=~"^{pod}.*"}}[30s]))*100'.format(pod=pod)
        response = self.promQL.queryRange(query, end)['data'][0]['values']
        return [[record[0], float(record[1])] for record in response]

    # pod的内存占用随时间变化[容器当前内存使用量/容器最大内存使用量]
    def getMemRate(self, pod: str, end: float):
        query = 'sum(container_memory_usage_bytes{{pod=~"^{pod}.*"}} ' \
                '/ container_memory_max_usage_bytes{{pod=~"^{pod}.*"}})/2'.format(pod=pod)
        response = self.promQL.queryRange(query, end)['data'][0]['values']
        return [[record[0], float(record[1])] for record in response]

    # pod所属的服务器节点
    def getNodeFromPod(self, pod: str):
        query = 'kube_pod_info{{namespace="openfaas-fn", pod=~"^{pod}.*"}}'.format(pod=pod + '-')
        return self.promQL.query(query)['data'][0]['metric']['node']


if __name__ == '__main__':
    promQL = PromQL('10.60.150.24:31119')
    cadvisor = CAdvisor(promQL)
    print(cadvisor.getDynamicInfoFromPod('add'))
