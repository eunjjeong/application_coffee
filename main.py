from PyQt5.QtWidgets import QApplication

from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao
from db_connection.connection_pool import ConnectionPool
from ui.coffee_form import CoffeeForm


def setting_main():
    app = QApplication([])
    w = CoffeeForm()
    app.exec_()


if __name__ == "__main__":
    setting_main()
    # DB연결 확인
    # pool = ConnectionPool.get_instance()
    # connection = pool.get_connection()
    # print(pool, connection)

    pdt = ProductDao()
    # pdt.select_code()
    # pdt.delete_item('C001')
    res = pdt.select_item()
    # print(res)
    sad = SaleDao()
    # sad.insert_item(5, 'C001', 5000, 10, 12)
    res = sad.select_item()
    # print(res)
    # res = sad.insert_item(5, 'C001', 4500, 150, 10)
    # print(res)
    res = sad.call_procedure()
    # print(type(res), res)
    # res = sad.procedure_item()
    # print(res)

    # sad.insert_product()
    # sad.delete_product()
    # sad.select()
    # sad.update_product()

    # res = pdt.insert_product('C001', '비스킷')
    # print(res)
    #
    # res = pdt.update_product(code='C001', name='비스킷2')
    # print(res)
    #
    # res = pdt.delete_product(code='C001')
    # print(res)
    #
    # res = pdt.select_product()
    # [print(code, name) for code, name in res]
    #
    # res = pdt.select_product(code='A%')
    # [print(code, name) for code, name in res]