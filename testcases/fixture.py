import requests
from jsonpath import jsonpath

from common.handle_conf import conf


class BaseTest:

    # member_id = None
    # headers = None

    @classmethod
    def admin_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        params2 = {
            'mobile_phone': conf.get('test_data', 'admin_mobile'),
            'pwd': conf.get('test_data', 'admin_pwd')
        }
        headers = eval(conf.get('env', 'headers'))

        res2 = requests.post(url=url, json=params2, headers=headers).json()

        admin_token = jsonpath(res2, '$..token')[0]

        cls.admin_member_id = jsonpath(res2, '$..id')[0]

        admin_headers = eval(conf.get('env', 'headers'))
        admin_headers['Authorization'] = 'Bearer ' + admin_token
        cls.admin_headers = admin_headers

    @classmethod
    def user_login(cls):
        url = conf.get('env', 'base_url') + '/member/login'
        params1 = {
            'mobile_phone': conf.get('test_data', 'mobile'),
            'pwd': conf.get('test_data', 'pwd')
        }

        headers = eval(conf.get('env', 'headers'))
        res1 = requests.post(url=url, json=params1, headers=headers).json()
        token = jsonpath(res1, '$..token')[0]
        cls.member_id = jsonpath(res1, '$..id')[0]
        headers['Authorization'] = 'Bearer ' + token
        cls.headers = headers

    @classmethod
    def add_project(cls):
        url = conf.get('env', 'base_url') + "/loan/add"
        params = {"member_id": cls.member_id,
                  "title": "借钱实现财富自由",
                  "amount": 2000,
                  "loan_rate": 12.0,
                  "loan_term": 3,
                  "loan_date_type": 1,
                  "bidding_days": 5}

        res = requests.post(url=url, json=params, headers=cls.headers).json()

        cls.loan_id = jsonpath(res, '$..id')[0]

    @classmethod
    def audit(cls):
        url = conf.get('env', 'base_url') + "/loan/audit"
        params = {"loan_id": cls.loan_id,
                  "approved_or_not": True
                  }

        res = requests.patch(url=url, json=params, headers=cls.admin_headers).json()

        # cls.loan_id = jsonpath(res, '$..id')[0]
