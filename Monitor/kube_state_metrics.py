from prometheus import PromQL


# 对应kube-state-metrics服务,监控k8s资源对象级别的指标
class KubeState:
    def __init__(self, prom: PromQL):
        self.promQL = prom

    # k8s集群中的服务器-node-ip
    def getNodes(self):
        res = {'status': 'error', 'nodes': []}
        response = self.promQL.query('kube_node_info')
        res['status'] = response['status']
        res['nodes'] = [{
            'ip': record['metric']['internal_ip'],
            'node': record['metric']['node']
        } for record in response['data']]
        return res

    # 服务器节点上启动的pod
    def getPodsFromNode(self, node: str):
        res = {'status': 'error', 'pod_name': []}
        query = 'kube_pod_info{{namespace="openfaas-fn", node="{node}"}}'.format(node=node)
        response = self.promQL.query(query)
        res['status'] = response['status']
        res['pod_name'] = [record['metric']['pod'].split('-')[0] for record in response['data']]
        return res

    # 集群中所有的pod
    def getPods(self):
        res = {'status': 'error', 'pods': []}
        response = self.promQL.query('kube_pod_info{namespace="openfaas-fn"}')
        res['status'] = response['status']
        res['pods'] = [{
            'pod_name': record['metric']['pod'].split('-')[0],
            'node': record['metric']['node']
        } for record in response['data']]
        return res


if __name__ == '__main__':
    promQL = PromQL('10.60.150.24:31119')
    kubeState = KubeState(promQL)
    print(kubeState.getPods())
