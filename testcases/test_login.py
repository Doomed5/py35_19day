import os
import unittest
import requests
from unittestreport import ddt, list_data
from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_tools import replace_data
from common.handler_log import my_log


@ddt
class TestLogin(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'login')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))
    print(headers)

    @list_data(cases)
    def test_login(self, item):
        url = self.base_url + item['url']
        # params = eval(item['data'])
        params = eval(replace_data(item['data'],TestLogin))
        method = item['method']
        expected = eval(item['excepted'])
        res = requests.request(method, url, json=params, headers=self.headers).json()
        try:
            # self.assertEqual(expected['code'],res['code'])
            # self.assertEqual(expected['msg'],res['msg'])
            self.assertDictIn(expected, res)
        except AssertionError as e:
            my_log.error('--用力【{}】--执行失败'.format(item['title']))
            my_log.error(e)
            raise e
        else:
            my_log.error('--用力【{}】--执行成功'.format(item['title']))

    def assertDictIn(self, excepted, res):
        for k, v in excepted.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(excepted, res))
