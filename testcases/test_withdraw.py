import os
import unittest

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_tools import replace_data
from common.handler_log import my_log
from common.handle_mysql import HandleDb


@ddt
class TestWithdraw(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'withdraw')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))
    db = HandleDb()

    @classmethod
    def setUpClass(cls) -> None:
        url = conf.get('env', 'base_url') + '/member/login'
        params = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }
        headers = cls.headers
        res = requests.post(url=url, json=params, headers=headers).json()
        token = jsonpath(res, '$..token')[0]
        cls.headers['Authorization'] = 'Bearer ' + token
        cls.member_id = str(jsonpath(res, '$..id')[0])
        # print(token)

    @list_data(cases)
    def test_withdraw(self, item):
        url = self.base_url + item['url']
        # item['data'] = item['data'].replace("#member_id#", self.member_id)
        item['data'] = replace_data(item['data'], TestWithdraw)
        params = eval(item['data'])
        excepted = eval(item['excepted'])

        sql = 'select leave_amount from future.member where mobile_phone="{}"'.format(conf.get('test_data', 'mobile'))
        start_amount = self.db.find_one(sql)[0]
        print(start_amount)
        res = requests.request(method=item['method'], url=url, json=params, headers=self.headers).json()
        print(excepted)
        print(res)
        end_amount = self.db.find_one(sql)[0]
        print(end_amount)
        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            if res['msg'] == 'OK':
                self.assertEqual(params['amount'], float(start_amount - end_amount))
            else:
                self.assertEqual(0, float(start_amount - end_amount))

        except AssertionError as e:
            my_log.error('--用例【{}】--执行失败'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.error('--用例【{}】--执行失败'.format(item['title']))
