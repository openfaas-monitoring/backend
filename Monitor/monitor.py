from Monitor.prometheus import PromQL
from Monitor.cadvisor import CAdvisor
from Monitor.func_monitor import FunctionMonitor
from Monitor.kube_state_metrics import KubeState
from Monitor.node_exporter import NodeExporter
from Monitor.func_logger import FunctionLogger
from Monitor.func_manager import FunctionManager


# 总体的监控器对象，负责对接其他不同层面的监控器对象
class Monitor:
    def __init__(self, node_info):
        self.ip = None
        self.promQL = None
        self.cadvisor = None
        self.functionMonitor = None
        self.kubeState = None
        self.nodeExporter = None
        self.functionLogger = None
        self.functionManager = None
        self.nodeInfo = node_info

    def setIP(self, ip):
        self.ip = ip
        self.promQL = PromQL(ip)
        if self.promQL.validConnection():
            self.cadvisor = CAdvisor(self.promQL)
            self.functionMonitor = FunctionMonitor(self.promQL, self.nodeInfo)
            self.kubeState = KubeState(self.promQL)
            self.nodeExporter = NodeExporter(self.promQL)
            self.functionLogger = FunctionLogger('./resource/kubeconfig.yml')
            self.functionManager = FunctionManager('/root/openfaas-workspace')
            return True
        else:
            return False

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

    # 获取函数日志
    def getLogsFromFunction(self, func: str):
        return self.functionLogger.getLogsFromFunction(func)

    # 获取函数源码级别信息
    def getSourceInfoFromFunction(self, func: str):
        return self.functionManager.getSourceInfo(func)


if __name__ == '__main__':
    monitor = Monitor({
        'vm-8c16g-node10': '10.60.150.24',
        'vm-2c4g-node6': '10.60.150.54',
        'vm-2c4g-node5': '10.60.150.55',
    })
    monitor.setIP('10.60.150.24:31119')
    # print(monitor.getDynamicInfoFromPod('nodeinfo'))
    print(monitor.getDynamicInfoFromNode('vm-2c4g-node6'))
