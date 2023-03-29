import os
import unittest

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data

from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handler_log import my_log
from common.handle_tools import replace_data
from common.handle_mysql import HandleDb

@ddt
class TestAdd(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'add')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))
    db =  HandleDb()
    @classmethod
    def setUpClass(cls) -> None:
        url = cls.base_url + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }
        # headers = eval(conf.get('env','headers'))
        res = requests.post(url=url, json=params, headers=cls.headers).json()
        token = jsonpath(res, '$..token')[0]
        print(token)
        cls.headers['Authorization'] = 'Bearer ' + token
        cls.member_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def test_add(self, item):
        url = self.base_url + item['url']
        params = eval(replace_data(item['data'], TestAdd))
        excepted = eval(item['excepted'])

        sql = 'select * from future.loan where member_id={}'.format(self.member_id)
        start_count = self.db.find_count(sql)
        print("调用接口之前的项目个数：",start_count)

        res = requests.request(method=item['method'], url=url, json=params, headers=self.headers).json()
        end_count = self.db.find_count(sql)
        print('调用接口之后的项目个数：',end_count)
        print(excepted)
        print(res)

        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            if res['code'] == 0:
                self.assertEqual(1,end_count-start_count)
            else:
                self.assertEqual(0, end_count - start_count)

        except Exception as e:
            my_log.error('--用例--【{}】--执行失败--'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.info('--用例--【{}】--执行成功--'.format(item['title']))
