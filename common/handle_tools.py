import re

from common.handle_conf import conf


def replace_data(data, cls):
    """

    :param data: 要进行替换的用例数据（字符串）
    :param cls: 测试类
    :return:
    """
    while re.search('#(.+?)#', data):
        res = re.search('#(.+?)#', data)
        item = res.group()
        attr = res.group(1)
        try:
            value = getattr(cls, attr)
        except AttributeError:
            value = conf.get('test_data', attr)
        data = data.replace(item, str(value))
    return data


if __name__ == '__main__':
    class TestData:
        id = 123
        name = 'musen'
        data = '121'
        title = '测试数据'


    s = '{"id":"#id#","name":"#name#","data":"#data#","title":"#title#","aaa":11,"bbb":22}'
    res = replace_data(s, TestData)
    print(res)
