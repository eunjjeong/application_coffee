import inspect
from mysql.connector import Error
from dao.abs_dao import Dao

insert_sql = "insert into product values(%s, %s)"
update_sql = "update product set name = %s where code = %s"
delete_sql = "delete from product where code = %s"
select_sql = "select code, name from product"
select_sql_where = select_sql + " where code = %s"
select_sql_code = "select code from product"

class ProductDao(Dao):

    def insert_item(self, code=None, name=None):
        print("\n______ {}() ______".format(inspect.stack()[0][3]))
        args = (code, name)
        try:
            super().do_query(query=insert_sql, kargs=args)
            print(code, name, "을 추가하였습니다.")
            return True
        except Error:
            return False

    def update_item(self, code=None, name=None):
        print("\n______ {}() ______".format(inspect.stack()[0][3]))
        args = (code, name)
        try:
            self.do_query(query=update_sql, kargs=args)
            print(name, "을 수정하였습니다.")
            return True
        except Error:
            return False

    def delete_item(self, code=None):
        print("\n______ {}() ______".format(inspect.stack()[0][3]))
        args = (code,)
        try:
            self.do_query(query=delete_sql, kargs=args)
            print("code = ", code, "를 삭제하였습니다.")
            return True
        except Error:
            return False

    def select_item(self, code=None):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql) if code is None else cursor.execute(select_sql_where, (code,))
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            # print(res)
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def select_code(self, code=None):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(select_sql_code)
            res = []
            [res.append(row) for row in self.iter_row(cursor, 5)]
            # print(res)
            return res
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()



