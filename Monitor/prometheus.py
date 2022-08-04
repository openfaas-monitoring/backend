import requests
import json


# 提供PromQL的统一查询接口，供其他指标监控类调用
class PromQL:
    def __init__(self, ip: str):
        self.ip = ip
        self.api = 'http://' + ip + '/api/v1/query'

    def query(self, query: str):
        res = {
            'status': "error",
            'data': '',
        }
        response = requests.get(self.api, {'query': query})
        if response.status_code == 200:
            response_json = json.loads(response.text)
            res['status'] = response_json['status']
            res['data'] = response_json['data']['result']
        else:
            print("请求错误,错误代码为" + str(response.status_code))

        return res


if __name__ == '__main__':
    promQL = PromQL('10.60.150.24:31119')
    promQL.query('http_requests_total{}[5m]')
