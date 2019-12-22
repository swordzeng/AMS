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
                    return QtCore.QVariant(QtCore.Qt.AlignLeft) 
                else:
                    return QtCore.QVariant(QtCore.Qt.AlignRight) 

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
                else:
                    return QtCore.QVariant('%.2f'%self._df.iloc[index.row(), index.column()]) 

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

class FloatDelegate(QtWidgets.QItemDelegate):
    def __init__(self, decimals, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent=parent)
        self.nDecimals = decimals

    def paint(self, painter, option, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        try:
            number = float(value)
            painter.drawText(option.rect, QtCore.Qt.AlignLeft, "{:.{}f}".format(number, self.nDecimals))
        except :
            QtWidgets.QItemDelegate.paint(self, painter, option, index)
