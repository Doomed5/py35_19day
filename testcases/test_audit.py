import os
import unittest

import requests
from jsonpath import jsonpath
from unittestreport import ddt, list_data

from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_mysql import HandleDb
from common.handle_path import DATA_DIR
from common.handle_tools import replace_data
from common.handler_log import my_log


@ddt
class TestAudit(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'audit')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')

    db = HandleDb()

    @classmethod
    def setUpClass(cls) -> None:
        url = cls.base_url + '/member/login'
        params1 = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }

        params2 = {
            'mobile_phone': conf.get('test_data', 'admin_mobile'),
            'pwd': conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'headers'))
        res1 = requests.post(url=url, json=params1, headers=headers).json()
        res2 = requests.post(url=url, json=params2, headers=headers).json()
        token = jsonpath(res1, '$..token')[0]
        admin_token = jsonpath(res2, '$..token')[0]
        cls.member_id = jsonpath(res1, '$..id')[0]
        cls.admin_member_id = jsonpath(res2, '$..id')[0]
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers
        # print(cls.headers)
        admin_headers = eval(conf.get('env', 'headers'))
        admin_headers['Authorization'] = 'Bearer ' + admin_token
        cls.admin_headers = admin_headers
        # print(cls.headers)
        # print(cls.admin_headers)

    def setUp(self) -> None:
        url = self.base_url + "/loan/add"
        params = {"member_id": self.member_id,
                  "title": "借钱实现财富自由",
                  "amount": 2000,
                  "loan_rate": 12.0,
                  "loan_term": 3,
                  "loan_date_type": 1,
                  "bidding_days": 5}

        res = requests.post(url=url, json=params, headers=self.headers).json()

        TestAudit.loan_id = jsonpath(res, '$..id')[0]

    @list_data(cases)
    def test_audit(self, item):
        url = self.base_url + item['url']
        params = eval(replace_data(item['data'], TestAudit))
        excepted = eval(item['excepted'])
        res = requests.request(method=item['method'], url=url, json=params, headers=self.admin_headers).json()
        print('预期', excepted)
        print('实际', res)
        if item['title'] == '审核通过' and res['msg'] == 'OK':
            TestAudit.pass_loan_id = self.loan_id

        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            if item['check_sql']:
                sql = item['check_sql'].format(self.loan_id)
                status = self.db.find_one(sql)[0]
                # print('数据库中的状态', status)
                # print(excepted['status'])
                self.assertEqual(excepted['status'], status)
        except AssertionError as e:
            my_log.error('用例--【{}】--执行失败'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.error('用例--【{}】--执行通过'.format(item['title']))
