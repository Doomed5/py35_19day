import unittest

from unittestreport import TestRunner

from common.handle_path import TASTCASES_DIR, REPORT_DIR

suite = unittest.defaultTestLoader.discover(TASTCASES_DIR)

runner = TestRunner(suite,
                    filename="py35.html",
                    report_dir=REPORT_DIR,
                    )

runner.run()
