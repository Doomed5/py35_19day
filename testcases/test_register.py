import os
import random
import unittest

import requests
from unittestreport import ddt, list_data

from common.handle_conf import conf
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handler_log import my_log
from common.handle_mysql import HandleDb


@ddt
class TestRegister(unittest.TestCase):
    excel = HandleExcel(os.path.join(DATA_DIR, 'cases.xlsx'), 'register')
    cases = excel.read_data()
    base_url = conf.get('env', 'base_url')
    headers = eval(conf.get('env', 'headers'))
    db = HandleDb()

    @list_data(cases)
    def test_register(self, item):
        url = self.base_url + item['url']
        if '#mobile_phone#' in item['data']:
            phone = self.random_mobile()
            item["data"] = item["data"].replace('#mobile_phone#', str(phone))
        params = eval(item['data'])
        method = item['method']
        excepted = eval(item['excepted'])
        # try:
        #     sql = 'select mobile_phone from future.member where mobile_phone={}'.format(params['mobile_phone'])
        #     start_reg = self.db.find_one(sql)[0]
        #     print('已注册：' + start_reg)
        # except:
        #     print('未注册')

        res = requests.request(method=method, url=url, json=params, headers=self.headers).json()
        print("预期：", excepted)
        print("实际", res)
        # sql = 'select mobile_phone from future.member where mobile_phone={}'.format(params.get('mobile_phone'),'')
        if item['check_sql']:
            sql = item['check_sql'].format(params.get('mobile_phone'),'')
            count = self.db.find_count(sql)

        try:
            self.assertEqual(excepted['code'], res['code'])
            self.assertEqual(excepted['msg'], res['msg'])
            if res['msg'] == "OK":
                print('数据库中查到的数量',count)
                self.assertEqual(1, count)

        except AssertionError as  e:
            my_log.error('用例--【{}】--执行失败'.format(item['title']))
            # my_log.exception(e)
            my_log.error(e)
            raise e
        else:
            my_log.error('用例--【{}】--执行通过'.format(item['title']))

    def random_mobile(self):
        mobile = str(random.randint(13300000000, 13399999999))
        return mobile
