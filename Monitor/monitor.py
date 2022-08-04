from prometheus import PromQL
from cadvisor import CAdvisor
from func_monitor import FunctionMonitor
from kube_state_metrics import KubeState
from node_exporter import NodeExporter


# 总体的监控器对象，负责对接其他不同层面的监控器对象
class Monitor:
    def __init__(self, ip):
        self.ip = ip
        self.promQL = PromQL(ip)
        self.cadvisor = CAdvisor(self.promQL)
        self.functionMonitor = FunctionMonitor(self.promQL)
        self.kubeState = KubeState(self.promQL)
        self.nodeExporter = NodeExporter(self.promQL)

    # 获取函数列表
    def getFunctions(self):
        return self.functionMonitor.getFunctions()

    # 获取函数静态信息
    def getStaticInfoFromFunction(self, func: str):
        return self.functionMonitor.getStaticInfoFromFunction(func)

    # 获取函数动态信息
    def getDynamicInfoFromFunction(self, func: str):
        return self.functionMonitor.getDynamicInfoFromFunction(func)

    # 获取pod列表
    def getPods(self):
        return self.kubeState.getPods()

    # 获取pod的静态信息
    def getStaticInfoFromPod(self, pod: str):
        return self.cadvisor.getStaticInfoFromPod(pod)

    # 获取pod的动态信息
    def getDynamicInfoFromPod(self, pod: str):
        return self.cadvisor.getDynamicInfoFromPod(pod)

    # 获取服务器列表
    def getNodes(self):
        return self.kubeState.getNodes()

    # 获取服务器上的pod
    def getPodsFromNode(self, node: str):
        return self.kubeState.getPodsFromNode(node)

    # 获取服务器动态信息
    def getDynamicInfoFromNode(self, node: str):
        return self.nodeExporter.getDynamicInfoFromNode(node)


if __name__ == '__main__':
    monitor = Monitor('10.60.150.24:31119')
    # print(monitor.getDynamicInfoFromPod('nodeinfo'))
    print(monitor.getDynamicInfoFromNode('vm-2c4g-node6'))
