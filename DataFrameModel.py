from PyQt5 import QtCore, QtWidgets, QtGui
import pandas as pd

class PandasModel(QtCore.QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            if role == QtCore.Qt.ForegroundRole:
                try:
                    value = float(self._df.iloc[index.row(), index.column()])
                except BaseException:
                    return QtCore.QVariant()
                else:
                    if value < 0:
                        return QtCore.QVariant(QtGui.QBrush(QtCore.Qt.red)) 

            if role == QtCore.Qt.TextAlignmentRole:       
                try:
                    value = float(self._df.iloc[index.row(), index.column()])
                except BaseException:
                    return QtCore.QVariant(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter) 
                else:
                    return QtCore.QVariant(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter) 

            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.DisplayRole:
            try:
                value = float(self._df.iloc[index.row(), index.column()])
            except BaseException:
                return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
            else:
                if list(self._df.columns)[index.column()].upper().find('RATIO') >= 0:
                    return QtCore.QVariant(format(self._df.iloc[index.row(), index.column()],'.2%'))
                elif list(self._df.columns)[index.column()].find('ID') >= 0:
                    return QtCore.QVariant('%.0f'%self._df.iloc[index.row(), index.column()])
                elif list(self._df.columns)[index.column()].find('Year') >= 0:
                    return QtCore.QVariant('%.0f'%self._df.iloc[index.row(), index.column()])
                elif list(self._df.columns)[index.column()].find('Month') >= 0:
                    return QtCore.QVariant('%.0f'%self._df.iloc[index.row(), index.column()])
                elif list(self._df.columns)[index.column()].find('Price') >= 0:
                    return QtCore.QVariant('%.3f'%self._df.iloc[index.row(), index.column()])
                else:
                    return QtCore.QVariant(format(self._df.iloc[index.row(), index.column()],'0,.2f'))

        #return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


def FormatView(view,columnCount=0):
    view.setSortingEnabled(True)
    view.verticalHeader().setHidden(True)
    #水平方向，表格大小拓展到适当的尺寸      
    #view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    if columnCount != 0:
        view.horizontalHeader().setSectionResizeMode(columnCount-1, QtWidgets.QHeaderView.Stretch)
    view.resizeColumnsToContents()
    view.setAlternatingRowColors(True)
    view.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
    #view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

def addActionColumn(tableView, model, tableName, func):
    columnPos = model.columnCount() - 1
    tableView.setColumnHidden(columnPos, False)

    rowCount = model.rowCount()
    for row in range(rowCount):
        iconDelete = QtGui.QIcon()
        iconDelete.addFile('logo/delete1.png')
        btnDelete = QtWidgets.QPushButton('')
        btnDelete.setIcon(iconDelete)
        btnDelete.clicked.connect(lambda:func(model))
        SymbolCode = model.itemData(model.index(row,0))[0]  #返回dict类型
        btnDelete.setProperty("row", row)    
        tableView.setIndexWidget(model.index(row,columnPos), btnDelete) 

def load_table(tableView, model, df):
    #db = sqlite3.connect('AMS.db')
    #query = "select * from " + tableName + condition
    #df = pd.read_sql(query, con = db)
    rowCount = df.shape[0]
    columnCount = df.shape[1]
    model.setRowCount = rowCount
    model.setColumnCount = columnCount + 1  #添加一列作为操作列，默认不显示
    headName = list(df)
    headName.append('Action')
    model.setHorizontalHeaderLabels(headName)
    for row in range(rowCount):
        for column in range(columnCount):
            item = QtGui.QStandardItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            
            itemValue = df.iloc[row,column]
            if type(itemValue).__name__ == 'int64':
                itemValue = int(itemValue)
            if type(itemValue).__name__ == 'float64':
                itemValue = float(itemValue)
                if itemValue < 0:
                    item.setForeground(QBrush(QColor(255, 0, 0)))
                itemValue = '{:.2f}'.format(itemValue)
            
            '''
            try:
                itemValue = float(df.iloc[row,column])
            except BaseException:
                itemValue = df.iloc[row,column]
            else:
                itemValue = QVariant('%.2f'%df.iloc[row,column])
                if itemValue < 0:
                    item.setForeground(QBrush(QColor(255, 0, 0)))
            '''
            item.setData(itemValue, QtCore.Qt.DisplayRole)
            #item.setEditable(False)
            model.setItem(row, column, item)

    tableView.setModel(model)

    tableView.setColumnHidden(columnCount, True)    #默认隐藏action列
    tableView.verticalHeader().setHidden(True)      #隐藏行号
    tableView.setSortingEnabled(True)
    #水平方向标签拓展剩下的窗口部分，填满表格
    #tableWidget.horizontalHeader().setStretchLastSection(True)
    #水平方向，表格大小拓展到适当的尺寸      
    tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    tableView.resizeColumnsToContents()
    tableView.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
