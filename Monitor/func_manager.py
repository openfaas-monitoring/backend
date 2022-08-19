import json


# 管理函数文件级别的静态信息，包括源码，流程配置文件等
class FunctionManager:
    def __init__(self, work_dir: str):
        self.work_dir = work_dir

    # 获取函数源码级别静态信息
    def getSourceInfo(self, func: str):
        res = {'status': 'success',
               'source_code': self.getSourceCode(func),
               'config': self.getConfigAndExplain(func)}

        return res

    # 获取函数源码
    def getSourceCode(self, func: str):
        path = '{}/{}/handler.py'.format(self.work_dir, func)
        with open(path, 'r') as f:
            code = f.readlines()
            code = ''.join(code)
        return code

    # 获取函数流程配置并解析
    def getConfigAndExplain(self, func: str):
        path = '{}/{}/process-cfg.json'.format(self.work_dir, func)
        with open(path, 'r') as f:
            config_json = json.load(f)

        process = []
        wait_join = dict()
        last_func = dict()
        for thread_name in config_json['thread_process']:
            wait_join[thread_name] = []
            last_func[thread_name] = []
        wait_join['main'] = []
        last_func['main'] = []

        for thread_name, thread_process in config_json['thread_process'].items():
            for func_info in thread_process:
                func_type = func_info['type']
                condition = func_info['condition']
                if func_type == 'order' and func_info['next_func_true'] == '':
                    last_func[thread_name].append(thread_name + '-' + func_info['func_name'])
                    continue
                if func_type == 'loop' and func_info['next_func_true'] == '':
                    process.append([thread_name + '-' + func_info['func_name'],
                                    thread_name + '-' + func_info['next_func_false'],
                                    condition + ' is False'])
                    last_func[thread_name].append(thread_name + '-' + func_info['func_name'])
                    continue
                if func_type == 'loop' and func_info['next_func_false'] == '':
                    process.append([thread_name + '-' + func_info['func_name'],
                                    thread_name + '-' + func_info['next_func_true'],
                                    condition + ' is True'])
                    last_func[thread_name].append(thread_name + '-' + func_info['func_name'])
                    continue

                if func_info['func_name'] == 'join':
                    wait_join[thread_name].append(func_info)
                    continue

                func_name = thread_name + '-' + func_info['func_name']
                next_func_true = thread_name + '-' + func_info['next_func_true']
                next_func_false = thread_name + '-' + func_info['next_func_false']

                if func_type == 'order':
                    process.append([func_name, next_func_true, ''])
                elif func_type == 'loop' or func_type == 'branch':
                    process.append([func_name, next_func_true, condition + ' is True'])
                    process.append([func_name, next_func_false, condition + ' is False'])

        for thread_name, func_join_infos in wait_join.items():
            for func_join_info in func_join_infos:
                for wait_thread in func_join_info['wait_threads']:
                    for one_last in last_func[wait_thread]:
                        func_name = one_last
                        func_type = func_join_info['type']
                        condition = func_join_info['condition']
                        next_func_true = thread_name + '-' + func_join_info['next_func_true']
                        next_func_false = thread_name + '-' + func_join_info['next_func_false']

                        if func_type == 'order':
                            process.append([func_name, next_func_true, ''])
                        elif func_type == 'loop' or func_type == 'branch':
                            process.append([func_name, next_func_true, condition + ' is True'])
                            process.append([func_name, next_func_false, condition + ' is False'])

        return process


if __name__ == '__main__':
    funcManager = FunctionManager('../resource')
    print(funcManager.getConfig('loop'))
