from prometheus import PromQL


# 对应kube-state-metrics服务,监控k8s资源对象级别的指标
class KubeState:
    def __init__(self, prom: PromQL):
        self.promQL = prom

    # k8s集群中的服务器-node-ip
    def getNodes(self):
        res = {'status': '', 'data': []}
        response = self.promQL.query('kube_node_info')
        res['status'] = response['status']
        res['data'] = [{
            'ip': record['metric']['internal_ip'],
            'node': record['metric']['node']
        } for record in response['data']]

        return res


if __name__ == '__main__':
    promQL = PromQL('10.60.150.24:31119')
    kubeState = KubeState(promQL)
    print('getNodes:')
    print(kubeState.getNodes())
