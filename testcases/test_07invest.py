import os.path
import unittest

import requests
from unittestreport import ddt, list_data

from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_mysql import HandleDb
from common.handle_path import DATA_DIR
from common.handle_tools import replace_data
from common.handler_log import my_log
from testcases.fixture import BaseTest


@ddt
class TestInvest(unittest.TestCase, BaseTest):
    excel = HandleExcel(os.path.join(DATA_DIR, 'cases.xlsx'), "invest")
    cases = excel.read_data()
    db = HandleDb()

    @classmethod
    def setUpClass(cls) -> None:
        cls.admin_login()
        cls.user_login()
        cls.add_project()
        cls.audit()

    @list_data(cases)
    def test_invest(self, item):
        url = conf.get("env", "base_url") + item['url']
        params = eval(replace_data(item['data'], TestInvest))
        excepted = eval(item['excepted'])
        sql1 = 'select leave_amount from future.member where id="{}"'.format(self.member_id)
        sql2 = 'select id from future.invest where member_id="{}"'.format(self.member_id)
        sql3 = 'select id from future.financelog where pay_member_id="{}"'.format(self.member_id)
        if item['check_sql']:
            s_amount = self.db.find_one(sql1)[0]
            s_invest = self.db.find_count(sql2)
            s_financelog = self.db.find_count(sql3)

        res = requests.request(method=item['method'], url=url, json=params, headers=self.headers).json()
        if item['check_sql']:
            e_amount = self.db.find_one(sql1)[0]
            e_invest = self.db.find_count(sql2)
            e_financelog = self.db.find_count(sql3)
        try:
            self.assertEqual(excepted['code'], res['code'])
            # self.assertEqual(excepted['msg'], res['msg'])
            self.assertIn(excepted['msg'], res['msg'])
            if item['check_sql']:
                self.assertEqual(params['amount'], float(s_amount - e_amount))
                self.assertEqual(1, e_invest - s_invest)
                self.assertEqual(1, e_financelog - s_financelog)
        except AssertionError as e:
            my_log.error('用例--【{}】--执行失败'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.error('用例--【{}】--执行通过'.format(item['title']))
