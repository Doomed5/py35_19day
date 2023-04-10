import unittest

from unittestreport import TestRunner

from common.handle_path import TASTCASES_DIR, REPORT_DIR


def main():
    suite = unittest.defaultTestLoader.discover(TASTCASES_DIR)

    runner = TestRunner(suite,
                        filename="py35.html",
                        report_dir=REPORT_DIR,
                        tester='Doomed',
                        title='测试报告'
                        )

    runner.run()
    runner.send_email(
        host='smtp.qq.com',
        port=465,
        user='530316028@qq.com',
        password='ycshrygrofgpbjhi',
        to_addrs='530316028@qq.com',
        is_file=True
    )


if __name__ == '__main__':
    main()
