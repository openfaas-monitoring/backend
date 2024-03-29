#  列表

```
url:http://10.60.150.24:8000/
```

> - 均使用get方法
> - 每个接口返回的json中均有status字段，只有当该字段值为success时，数据才有效
> - 其中随时间变化的数据均为二维数组形式，数组中是一个二元组，前者表示时间戳，后者表示具体的值。整体表示过去60s内，每秒采集一次指标，得到的长度为60的二维数组

提供的接口：

- `/setIP`：参数为ip，设置k8s的查询接口
- `/global/functions`：无参数，返回函数列表
- `/static/function`：参数为func，表示查询该函数的静态信息
- `/dynamic/function`：参数为func，表示查询该函数的动态信息
- `/global/pods`：无参数，返回pod列表
- `/static/pod`：参数为pod，表示查询该pod的静态信息
- `/dynamic/pod`：参数为pod，表示查询该pod的动态信息
- `/global/nodes`：无参数，返回物理机nodes列表
- `/dynamic/getPodsFromNode`：参数为node，表示查询该node上的pod列表
- `/dynamic/node`：参数为node，表示查询该node的动态信息

# 详细说明

## /setIP

返回连接结果，存在status字段。如果为success表示连接成功，返回出错或者error表示连接失败

eg：`http://10.60.150.24:8000/setIP?ip=10.60.150.24:31119`

```json
{
    "status": "success"
}
```

## /global/functions

返回函数列表

eg：`http://10.60.150.24:8000/global/functions`

```json
{
    "func": [
        "add",
        "nodeinfo"
    ],
    "status": "success"
}
```

## /static/function

提供参数func为函数名，返回函数的静态信息

eg：`http://10.60.150.24:8000/static/function?func=add`

```json
{
    "image": "evernorif/paralleltest:latest",
    "invocations": {
        "error": 6,
        "success": 8
    },
    "replicas": 1,
    "running_api": "10.60.150.54",
    "status": "success"
}
```

- 镜像位置
- 调用次数【包括失败和成功的次数】
- 副本个数
- running_api：应该向这个url请求running信息

## /dynamic/function

eg：`http://10.60.150.24:8000/dynamic/function?func=nodeinfo`

```json
{
    "cpuRate": [[],...]
    "func_time": 8.351746,
    "memRate": [[],...]
    "request_time": 0.368262837009145,
    "status": "success"
}
```

- CPU占用率随时间变化
- 内存占用率随时间变化
- 函数平均运行时间[ms]
- 函数平均响应时间[ms]

## /global/pods

eg：`http://10.60.150.24:8000/global/pods`

返回pods列表，以及pod的位置，在哪个物理机node上

```json
{
    "pods": [
        {
            "node": "vm-2c4g-node6",
            "pod_name": "branchtest",
            "pod_real_name": "branchtest-7f86ffcd8f-nlvqm"
        },
        {
            "node": "vm-2c4g-node5",
            "pod_name": "looptest",
            "pod_real_name": "looptest-68f9579f7c-2xk5z"
        },
        {
            "node": "vm-2c4g-node6",
            "pod_name": "ordertest",
            "pod_real_name": "ordertest-d64cb8d8c-n9vn2"
        },
        {
            "node": "vm-2c4g-node6",
            "pod_name": "parallel",
            "pod_real_name": "parallel-586fb669d5-d6g58"
        }
    ],
    "status": "success"
}
```



## /static/pod

eg：`http://10.60.150.24:8000/static/pod?pod=add`

提供pod名称

```json
{
    "node": "vm-2c4g-node5",
    "status": "success"
}
```

- pod在哪个node上

## /dynamic/pod

eg：`http://10.60.150.24:8000/dynamic/pod?pod=nodeinfo`

```json
{
    "cpuRate": [[]...],
    "memRate": [[]...],
    "status": "success"
}
```

- 该pod的cpu使用率随时间变化
- 该pod的内存使用率随时间变化（使用内存/最高限制内存）

## /global/nodes

eg：`http://10.60.150.24:8000/global/nodes`

```json
{
    "nodes": [
        {
            "ip": "10.60.150.24",
            "node": "vm-8c16g-node10"
        },
        {
            "ip": "10.60.150.54",
            "node": "vm-2c4g-node6"
        },
        {
            "ip": "10.60.150.55",
            "node": "vm-2c4g-node5"
        }
    ],
    "status": "success"
}
```

- 物理机列表，ip和hostname

## /dynamic/getPodsFromNode

eg：`http://10.60.150.24:8000/dynamic/getPodsFromNode?node=vm-2c4g-node6`

```json
{
    "pod_name": [
        "nodeinfo"
    ],
    "status": "success"
}
```

- 返回node上存在的pod列表

## /dynamic/node

eg：`http://10.60.150.24:8000/dynamic/node?node=vm-2c4g-node6`

```json
{
    "cpuRate": [[]...],
    "diskRate": [[]...],
    "diskRead": [[]...],
    "diskWrite": [[]...],
    "memRate": [[]...],
    "networkDown": [[]...],
    "networkUp": [[]...],
    "status": "success"
}
```

- CPU占用率随时间变化
- 磁盘占用率随时间变化
- 磁盘读速率随时间变化[kb]
- 磁盘写速率随时间变化[kb]
- 内存使用率随时间变化
- 网络下载速率随时间变化[kb]
- 网络上传速率随时间变化[kb]

## /logs

提供函数名func为参数，返回函数所有日志

eg：`http://10.60.150.24:8000/logs?func=errlog`

```json
{"logs":"2022/08/13 07:56:38 Version: 0.2.1\tSHA: cd8dc9f4e98049150d8079a74a18cd5a2e311aeb\n2022/08/13 07:56:38 Timeouts: read: 5s write: 5s hard: 0s health: 5s.\n2022/08/13 07:56:38 Listening on port: 8080\n2022/08/13 07:56:38 Writing lock-file to: /tmp/.lock\n2022/08/13 07:56:38 Metrics listening on port: 8081\n2022/08/13 07:56:47 Forking fprocess.\n2022/08/13 07:56:47 Query  \n2022/08/13 07:56:47 Path  /\n2022/08/13 07:56:47 Duration: 0.304398s\n2022/08/13 07:56:47 INFO handle started\n2022/08/13 07:56:47 INFO handle invoke function1\n2022/08/13 07:56:47 INFO function1 started\n2022/08/13 07:56:47 INFO function1 invoke function2\n2022/08/13 07:56:47 INFO function2 started\n2022/08/13 07:56:47 INFO function2 invoke function3\n2022/08/13 07:56:47 INFO function3 started\nhandle to test\n\n\n2022/08/13 08:01:36 Forking fprocess.\n2022/08/13 08:01:36 Query  \n2022/08/13 08:01:36 Path  /\n2022/08/13 08:01:36 Duration: 0.170497s\n2022/08/13 08:01:36 INFO handle started\n2022/08/13 08:01:36 INFO handle invoke function1\n2022/08/13 08:01:36 INFO function1 started\n2022/08/13 08:01:36 INFO function1 invoke function2\n2022/08/13 08:01:36 INFO function2 started\n2022/08/13 08:01:36 INFO function2 invoke function3\n2022/08/13 08:01:36 INFO function3 started\nhandle to test\n\n\n2022/08/13 08:10:01 Forking fprocess.\n2022/08/13 08:10:01 Query  \n2022/08/13 08:10:01 Path  /\n2022/08/13 08:10:01 INFO handle started\n2022/08/13 08:10:01 INFO handle invoke function1\n2022/08/13 08:10:01 INFO function1 started\n2022/08/13 08:10:01 INFO function1 invoke function2\n2022/08/13 08:10:01 INFO function2 started\n2022/08/13 08:10:01 INFO function2 invoke function3\n2022/08/13 08:10:01 INFO function3 started\nhandle to test\n\n\n2022/08/13 08:10:01 Duration: 0.168406s\n",
 "status":"success"}
```

## /source

提供函数func，返回函数的源码级别相关信息

eg：`http://10.60.150.24:8000/source?func=looptest`

返回信息

```json
{
    "config": [
        [
            "main-function1",
            "main-function2",
            ""
        ],
        [
            "main-function2",
            "main-function2",
            "flag1 is True"
        ],
        [
            "main-function2",
            "main-function3",
            "flag1 is False"
        ]
    ],
    "source_code": "from function import globalFlag\nimport time\n\n\ndef function1(args):\n    args['num1'] = args['std_in']\n    return args\n\n\ndef function2(args):\n    time.sleep(1)\n    args['num1'] = args['num1'] + args['num1']\n    if len(args['num1']) < 10:\n        globalFlag.set_value('flag1', True)\n    else:\n        globalFlag.set_value('flag1', False)\n\n    return args\n\n\ndef function3(args):\n    args['res'] = args['num1']\n    return args\n",
    "status": "success"
}
```

## /running

提供函数func，返回函数的运行信息

注意这里的接口url对应前面`/global/functions`中的running_api

【注意这里IP的不同】

eg：`http://10.60.150.54:8000/running?func=paralleltest`

```json
{
    "running_info": [
        "thread1-function1",
        "thread2-function2",
        "thread3-function3",
        "main-function4"
    ],
    "running_status": "stop",
    "status": "success"
}
```

```json
{
    "running_info": [
        "thread1-function1",
        "thread2-function2",
        "thread3-function3"
    ],
    "running_status": "running",
    "status": "success"
}
```

- running_info：当前需要标绿的节点
- running_status：当前函数是否在运行，分为running和stop两种状态



eg：`http://10.60.150.55:8000/running?func=looptest`

```json
{
    "running_info": [
        "main-function1",
        "main-function2",
        "main-function3"
    ],
    "running_status": "stop",
    "status": "success"
}
```

