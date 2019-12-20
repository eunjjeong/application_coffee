import re

from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QHeaderView, QTableWidgetItem, QAction, QMessageBox

from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao


def create_table(table=None, data=None):
    table.setHorizontalHeaderLabels(data)
    # row 단위로 선택
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 수정불가능
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 균일한 간격으로 재배치
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.horizontalHeader().setStyleSheet("Background-color:rgb(165, 212, 255);border-radius:15px;")
    return table


class CoffeeForm(QWidget):
    def __init__(self, data=None, header=None):
        super().__init__()
        self.ui = uic.loadUi("ui/coffee_form.ui")
        self.ui.show()

        self.ptable = create_table(table = self.ui.productTable, data = ["CODE", "NAME"])
        self.stable = create_table(table = self.ui.saleTable, data = ["NO", "CODE", "PRICE", "SALE COUNT", "MARGIN RATE"])
        self.sorttable = create_table(table=self.ui.sortTable, data=['RANK', 'CODE', 'NAME', 'PRICE', 'SALE COUNT', 'SUPPLY PRICE', 'ADDTAX', 'SALE PRICE', 'MARGIN RATE', 'MARGIN PRICE'])

        # product slot/signal
        self.ui.btn_padd.clicked.connect(self.add_prd)
        self.ui.btn_pupdate.clicked.connect(self.update_prd)
        self.ui.btn_pinit.clicked.connect(self.init_coffee)
        self.ui.btn_resetP.clicked.connect(self.init_resetP)

        self.set_context_menu(self.ptable)

        pdt = ProductDao()
        pdata = pdt.select_item
        self.pdata = pdata or [()]
        self.load_pdata(pdata)

        # sale slot/signal
        self.ui.btn_sadd.clicked.connect(self.add_sad)
        self.ui.btn_supdate.clicked.connect(self.update_sad)
        self.ui.btn_sinit.clicked.connect(self.init_coffee)
        self.ui.btn_resetS.clicked.connect(self.init_resetS)

        # sale combobox
        self.cmb_reset()

        self.set_context_smenu(self.stable)

        sad = SaleDao()
        sdata = sad.select_item
        self.sdata = sdata or [()]
        self.load_sdata(sdata)

        # sale sort
        self.ui.cnt_rbtn.setChecked(True)
        self.cnt_sort()
        self.ui.cnt_rbtn.clicked.connect(self.cnt_sort)
        self.ui.mr_rbtn.clicked.connect(self.margin_sort)

    def init_resetP(self):
        self.ptable.setRowCount(0)
        pdt = ProductDao()
        pdata = pdt.select_item
        self.pdata = pdata or [()]
        self.load_pdata(pdata)

    def load_pdata(self, data):
        for idx, (code, name) in enumerate(data()):
            item_code, item_name = self.create_prd(code, name)
            nextIdx = self.ptable.rowCount()
            self.ptable.insertRow(nextIdx)
            self.ptable.setItem(nextIdx, 0, item_code)
            self.ptable.setItem(nextIdx, 1, item_name)

    def set_context_menu(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction("수정", tv)
        delete_action = QAction("삭제", tv)
        tv.addAction(update_action)
        tv.addAction(delete_action)

        update_action.triggered.connect(self.__pupdate)
        delete_action.triggered.connect(self.__pdelete)

    def __pupdate(self):
        selectionIdx = self.ptable.selectedIndexes()[0]
        code = self.ptable.item(selectionIdx.row(), 0).text()
        name = self.ptable.item(selectionIdx.row(), 1).text()
        self.ui.le_pcode.setText(code)
        self.ui.le_name.setText(name)


    def __pdelete(self):
        selectionIdx = self.ptable.selectedIndexes()[0]
        code = self.ptable.item(selectionIdx.row(), 0).text()
        self.ptable.removeRow(selectionIdx.row())
        pdt = ProductDao()
        pdt.delete_item(code)
        self.cmb_reset()
        QMessageBox.information(self, 'DELETE', '삭제하였습니다.', QMessageBox.Ok)

    def add_prd(self):
        item_code, item_name = self.get_prd_form_le()
        currentIdx = self.ptable.rowCount()
        self.ptable.insertRow(currentIdx)
        self.ptable.setItem(currentIdx, 0, item_code)
        self.ptable.setItem(currentIdx, 1, item_name)
        self.init_coffee()
        self.cmb_reset()
        QMessageBox.information(self, 'ADD', '추가하였습니다.', QMessageBox.Ok)

    def get_prd_form_le(self):
        code = self.ui.le_pcode.text()
        name = self.ui.le_name.text()

        pdt = ProductDao()
        pdt.insert_item(code, name)

        return self.create_prd(code, name)

    def create_prd(self, code, name):
        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)
        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_code.setBackground(QtGui.QColor(141, 222, 255))
        return item_code, item_name

    def update_prd(self):
        selectionIdx = self.ptable.selectedIndexes()[0]
        code = self.ui.le_pcode.text()
        name = self.ui.le_name.text()
        self.ptable.item(selectionIdx.row(), 0).setText(code)
        self.ptable.item(selectionIdx.row(), 1).setText(name)
        pdt = ProductDao()
        pdt.update_item(name, code)
        self.init_coffee()
        self.cnt_sort()
        self.margin_sort()
        QMessageBox.information(self, 'UPDATE', '변경하였습니다.', QMessageBox.Ok)

    def init_coffee(self):
        self.ui.le_pcode.clear()
        self.ui.le_name.clear()

        self.ui.le_no.clear()
        self.ui.le_marginR.clear()
        self.ui.le_price.clear()
        self.ui.le_saleCnt.clear()
        self.ui.cmb_code.setCurrentIndex(0)


# sale
    def load_pdata_code(self, data):
        for idx, (code) in enumerate(data()):
            self.ui.cmb_code.addItem(str(code)[2:6])

    def init_resetS(self):
        self.stable.setRowCount(0)
        sad = SaleDao()
        sdata = sad.select_item
        self.sdata = sdata or [()]
        self.load_sdata(sdata)

    def load_sdata(self, data):
        for idx, (no, code, price, saleCnt, marginR) in enumerate(data()):
            item_no, item_code, item_price, item_saleCnt, item_marginR = self.create_sad(no, code, price, saleCnt, marginR)
            nextIdx = self.stable.rowCount()
            self.stable.insertRow(nextIdx)
            self.stable.setItem(nextIdx, 0, item_no)
            self.stable.setItem(nextIdx, 1, item_code)
            self.stable.setItem(nextIdx, 2, item_price)
            self.stable.setItem(nextIdx, 3, item_saleCnt)
            self.stable.setItem(nextIdx, 4, item_marginR)

    def set_context_smenu(self, tv):
        tv.setContextMenuPolicy(Qt.ActionsContextMenu)
        update_action = QAction("수정", tv)
        delete_action = QAction("삭제", tv)
        tv.addAction(update_action)
        tv.addAction(delete_action)

        update_action.triggered.connect(self.__supdate)
        delete_action.triggered.connect(self.__sdelete)

    def __supdate(self):
        selectionIdx = self.stable.selectedIndexes()[0]
        no = self.stable.item(selectionIdx.row(), 0).text()
        code = self.stable.item(selectionIdx.row(), 1).text()
        price = self.stable.item(selectionIdx.row(), 2).text()
        price = re.sub('[,]', '', price)
        saleCnt = self.stable.item(selectionIdx.row(), 3).text()
        marginR = self.stable.item(selectionIdx.row(), 4).text()
        marginR = re.sub('[%]', '', marginR)

        self.ui.le_no.setText(no)
        index = self.ui.cmb_code.findText(code)
        self.ui.cmb_code.setCurrentIndex(index)
        # self.ui.le_scode.setText(code)
        self.ui.le_price.setText(price)
        self.ui.le_saleCnt.setText(saleCnt)
        self.ui.le_marginR.setText(marginR)

    def __sdelete(self):
        selectionIdx = self.stable.selectedIndexes()[0]
        code = self.stable.item(selectionIdx.row(), 0).text()
        self.stable.removeRow(selectionIdx.row())
        sad = SaleDao()
        sad.delete_item(code)
        self.cnt_sort()
        self.margin_sort()
        QMessageBox.information(self, 'DELETE', '삭제하였습니다.', QMessageBox.Ok)

    def add_sad(self):
        item_no, item_code, item_price, item_saleCnt, item_marginR = self.get_sad_form_le()
        currentIdx = self.stable.rowCount()
        self.stable.insertRow(currentIdx)
        self.stable.setItem(currentIdx, 0, item_no)
        self.stable.setItem(currentIdx, 1, item_code)
        self.stable.setItem(currentIdx, 2, item_price)
        self.stable.setItem(currentIdx, 3, item_saleCnt)
        self.stable.setItem(currentIdx, 4, item_marginR)
        self.init_coffee()
        self.cnt_sort()
        self.margin_sort()
        QMessageBox.information(self, 'ADD', '추가하였습니다.', QMessageBox.Ok)

    def get_sad_form_le(self):
        no = self.ui.le_no.text()
        # code = self.ui.le_scode.text()
        code = self.ui.cmb_code.currentText()
        price = self.ui.le_price.text()
        saleCnt = self.ui.le_saleCnt.text()
        marginR = self.ui.le_marginR.text()

        sad = SaleDao()
        sad.insert_item(no, code, price, saleCnt, marginR)
        return self.create_sad(no, code, price, saleCnt, marginR)

    def create_sad(self, no, code, price, saleCnt, marginR):
        item_no = QTableWidgetItem()
        item_no.setTextAlignment(Qt.AlignCenter)
        item_no.setData(Qt.DisplayRole, no)

        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_price.setData(Qt.DisplayRole, format(int(price), ',d'))

        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignCenter)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)

        item_marginR = QTableWidgetItem()
        item_marginR.setTextAlignment(Qt.AlignCenter)
        item_marginR.setData(Qt.DisplayRole, str(marginR) + '%')

        item_code.setBackground(QtGui.QColor(141, 222, 255))
        return item_no, item_code, item_price, item_saleCnt, item_marginR

    def update_sad(self):
        selectionIdx = self.stable.selectedIndexes()[0]
        no = self.ui.le_no.text()
        # code = self.ui.le_scode.text()
        code = self.ui.cmb_code.currentText()
        price = self.ui.le_price.text()
        saleCnt = self.ui.le_saleCnt.text()
        marginR = self.ui.le_marginR.text()
        self.stable.item(selectionIdx.row(), 0).setText(no)
        self.stable.item(selectionIdx.row(), 1).setText(code)
        self.stable.item(selectionIdx.row(), 2).setText(format(int(price), ',d'))
        self.stable.item(selectionIdx.row(), 3).setText(saleCnt)
        self.stable.item(selectionIdx.row(), 4).setText(marginR + '%')
        sad = SaleDao()
        sad.update_item(code, price, saleCnt, marginR, no)
        self.init_coffee()
        self.cnt_sort()
        self.margin_sort()
        QMessageBox.information(self, 'UPDATE', '변경하였습니다.', QMessageBox.Ok)

# sale sort
    def load_sortdata(self, sortdata):
        for idx, (rank, code, name, price, saleCnt, supplyP, addTax, saleP, marginR, marginP) in enumerate(sortdata()):
            item_rank, item_code, item_name, item_price, item_saleCnt, item_supplyP, item_addTax, item_saleP, item_marginR, item_marginP \
                = self.create_sort(rank, code, name, price, saleCnt, supplyP, addTax, saleP, marginR, marginP)
            nextIdx = self.sorttable.rowCount()
            self.sorttable.insertRow(nextIdx)
            self.sorttable.setItem(nextIdx, 0, item_rank)
            self.sorttable.setItem(nextIdx, 1, item_code)
            self.sorttable.setItem(nextIdx, 2, item_name)
            self.sorttable.setItem(nextIdx, 3, item_price)
            self.sorttable.setItem(nextIdx, 4, item_saleCnt)
            self.sorttable.setItem(nextIdx, 5, item_supplyP)
            self.sorttable.setItem(nextIdx, 6, item_addTax)
            self.sorttable.setItem(nextIdx, 7, item_saleP)
            self.sorttable.setItem(nextIdx, 8, item_marginR)
            self.sorttable.setItem(nextIdx, 9, item_marginP)

    def create_sort(self, rank, code, name, price, saleCnt, supplyP, addTax, saleP, marginR, marginP):
        item_rank = QTableWidgetItem()
        item_rank.setTextAlignment(Qt.AlignCenter)
        item_rank.setData(Qt.DisplayRole, rank)

        item_code = QTableWidgetItem()
        item_code.setTextAlignment(Qt.AlignCenter)
        item_code.setData(Qt.DisplayRole, code)

        item_name = QTableWidgetItem()
        item_name.setTextAlignment(Qt.AlignCenter)
        item_name.setData(Qt.DisplayRole, name)

        item_price = QTableWidgetItem()
        item_price.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_price.setData(Qt.DisplayRole, format(price, ',d'))

        item_saleCnt = QTableWidgetItem()
        item_saleCnt.setTextAlignment(Qt.AlignCenter)
        item_saleCnt.setData(Qt.DisplayRole, saleCnt)

        item_supplyP = QTableWidgetItem()
        item_supplyP.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_supplyP.setData(Qt.DisplayRole, format(supplyP, ',d'))

        item_addTax = QTableWidgetItem()
        item_addTax.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_addTax.setData(Qt.DisplayRole, format(addTax, ',d'))

        item_saleP = QTableWidgetItem()
        item_saleP.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_saleP.setData(Qt.DisplayRole, format(saleP, ',d'))

        item_marginR = QTableWidgetItem()
        item_marginR.setTextAlignment(Qt.AlignCenter)
        item_marginR.setData(Qt.DisplayRole, str(marginR) + '%')

        item_marginP = QTableWidgetItem()
        item_marginP.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        item_marginP.setData(Qt.DisplayRole, format(marginP, ',d'))

        item_code.setBackground(QtGui.QColor(131, 222, 255))
        item_saleP.setBackground(QtGui.QColor(178, 243, 255))
        item_marginP.setBackground(QtGui.QColor(178, 243, 255))
        return item_rank, item_code, item_name, item_price, item_saleCnt, item_supplyP, item_addTax, item_saleP, item_marginR, item_marginP

    def cnt_sort(self):
        self.ui.sortTable.setRowCount(0)
        sad = SaleDao()
        sortdata = sad.call_procedure
        self.sortdata = sortdata or [()]
        self.load_sortdata(sortdata)

    def margin_sort(self):
        self.ui.sortTable.setRowCount(0)
        sad = SaleDao()
        sortdata = sad.call_procedure2
        self.sortdata = sortdata or [()]
        self.load_sortdata(sortdata)

    def cmb_reset(self):
        self.ui.cmb_code.clear()
        pdt = ProductDao()
        pcode = pdt.select_code
        self.pcode = pcode or [()]
        self.load_pdata_code(pcode)

