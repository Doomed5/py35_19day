import pymysql
from common.handle_conf import conf


class HandleDb:
    def __init__(self):
        self.con = pymysql.connect(
            host=conf.get('mysql', 'host'),
            port=eval(conf.get('mysql', 'port')),
            user=conf.get('mysql', 'user'),
            password=conf.get('mysql', 'password'),
            charset=conf.get('mysql', 'charset')
            # cursorclass=pymysql.cursors.DictCursor #设置游标对象返回的数据类型为字典，默认为元组
        )

    def find_all(self, sql):
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self, sql):
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self, sql):
        with self.con as cur:
            res = cur.execute(sql)
        cur.close()
        return res

    def __del__(self):
        self.con.close()


if __name__ == '__main__':
    sql = 'select * from future.member limit 5;'
    db = HandleDb()
    res = db.find_all(sql)
    print(res)
