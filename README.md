# openfaas-monitoring backend

监控平台的后端工程，部署在Master节点上的后端程序。

## Code Framework

- `Monitor`：监控模块
  - `monitor.py`：总体的监控对象，负责对接其他不同层面的监控器对象，作为统一的接口提供对象
  - `cadvisor.py`：对应cadvisor服务，监控容器级别的指标
  - `func_logger.py`：连接kubernetes集群，获取日志信息
  - `func_manager.py`：管理函数文件级别的静态信息，包括源码，流程配置文件等
  - `func_monitor.py`：对接openfaas-prometheus服务，监控函数级别的指标
  - `kube_state_metrics.py`：对应kube-state-metrics服务，监控kubernetes资源对象级别的指标
  - `node_exporter.py`：对应node-exporter服务，监控物理机器级别的指标
  - `prometheus.py`：提供Prometheus的统一查询服务，供其他指标监控类调用
- `backend.py`：整体后端代码的
- `resource`：通过python连接到kubernetes集群，所需的资源文件放在`resource`目录下。（这里实际的资源文件没有上传到github上）
- `interface.md`：接口文档

## Todo

OpenFaas服务层面：

- [x] 当前连接状态
- [x] 当前各个函数的状态
- [x] 提供的函数列表

函数层面：

- [x] 函数列表
- [x] 函数源码
- [x] 函数对应的镜像位置
- [x] 函数的副本数
- [x] 函数的历史调用次数
- [x] 函数的运行状态
- [x] 函数的平均运行时间
- [x] 函数的平均响应时间
- [x] 函数相互调用情况
- [x] 函数CPU占用率随时间变化
- [x] 函数内存占用率随时间变化
- [x] 函数的运行日志

容器层面：

- [x] 容器所属服务器节点
- [x] 容器CPU占用率随时间变化
- [x] 容器内存占用率随时间变化

服务器节点层面：

- [x] 当前集群中的服务器IP和Hostname
- [x] 节点CPU占用率随时间变化
- [x] 节点磁盘占用率随时间变化
- [x] 节点磁盘IO随时间变化
- [x] 节点内存占用率随时间变化
- [x] 节点网络IO随时间变化
- [x] 服务器上启动的对应容器



 
