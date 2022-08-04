from prometheus import PromQL, PrometheusCannotQuery
import time


# 对应node-exporter服务,监控物理机器级别的指标
class NodeExporter:
    def __init__(self, prom: PromQL):
        self.promQL = prom

    # 服务器相关动态信息查询
    def getDynamicInfoFromNode(self, node: str):
        end = time.time()
        res = dict()
        try:
            res['cpuRate'] = self.getCPURate(node, end)
            res['diskRate'] = self.getDiskRate(node, end)
            res['diskRead'] = self.getDiskRead(node, end)
            res['diskWrite'] = self.getDiskWrite(node, end)
            res['memRate'] = self.getMemRate(node, end)
            res['networkUp'] = self.getNetworkUpLoad(node, end)
            res['networkDown'] = self.getNetWorkDownload(node, end)

            res['status'] = 'success'
        except PrometheusCannotQuery:
            res['status'] = 'error'

        return res

    # 节点CPU使用率
    def getCPURate(self, node: str, end: float):
        query = '100-(avg by(instance)' \
                '(irate(node_cpu_seconds_total{{mode="idle",instance="{node}"}}[30s]))*100)'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']

    # 节点磁盘使用率
    def getDiskRate(self, node: str, end: float):
        query = '100 - ' \
                'node_filesystem_free_bytes{{mountpoint = "/", instance="{node}", ' \
                'fstype!~"rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs|udev|none|devpts|sysfs|debugfs|fuse.*"}} /' \
                'node_filesystem_size_bytes{{mountpoint = "/", instance="{node}", ' \
                'fstype!~"rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs|udev|none|devpts|sysfs|debugfs|fuse.*"}}' \
                ' * 100'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']

    # 节点磁盘IO[单位为kB]
    def getDiskRead(self, node: str, end: float):
        query = 'sum by(instance)(irate(node_disk_read_bytes_total{{instance="{node}"}}[30s])' \
                '/1024)'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']

    def getDiskWrite(self, node: str, end: float):
        query = 'sum by(instance)(irate(node_disk_written_bytes_total{{instance="{node}"}}[30s])' \
                '/1024)'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']

    # 节点内存使用率随时间变化图
    def getMemRate(self, node: str, end: float):
        query = '100 -(node_memory_MemFree_bytes{{instance="{node}"}} ' \
                '+ node_memory_Cached_bytes{{instance="{node}"}}' \
                '+node_memory_Buffers_bytes{{instance="{node}"}})' \
                '/node_memory_MemTotal_bytes{{instance="{node}"}}*100'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']

    # 节点网络IO[单位为KB]
    def getNetworkUpLoad(self, node: str, end: float):
        query = 'sum by(instance)' \
                '(irate(node_network_transmit_bytes_total{{device!="lo",instance="{node}"}}[30s])' \
                '/1024)'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']

    def getNetWorkDownload(self, node: str, end: float):
        query = 'sum by(instance)' \
                '(irate(node_network_receive_bytes_total{{device!="lo",instance="{node}"}}[30s])' \
                '/1024)'.format(node=node)
        return self.promQL.queryRange(query, end)['data'][0]['values']


if __name__ == '__main__':
    promQL = PromQL('10.60.150.24:31119')
    nodeExporter = NodeExporter(promQL)
    # print(nodeExporter.getDiskWrite('vm-2c4g-node5', time.time()))
    print(nodeExporter.getDynamicInfoFromNode('vm-2c4g-node5'))
