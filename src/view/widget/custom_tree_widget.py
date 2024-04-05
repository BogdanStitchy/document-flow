from PyQt5.QtCore import *
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import *


class CustomTreeWidget(QTreeWidget):
    customMimeType = "application/x-customTreeWidgetdata"

    def __init__(self):
        super().__init__()
        self.expandAll()
        self.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def mimeTypes(self):
        mimetypes = QTreeWidget.mimeTypes(self)
        mimetypes.append(CustomTreeWidget.customMimeType)
        return mimetypes

    def startDrag(self, supported_actions):
        drag = QDrag(self)
        mime_data = self.model().mimeData(self.selectedIndexes())

        encoded = QByteArray()
        stream = QDataStream(encoded, QIODevice.WriteOnly)
        self.encode_data(self.selectedItems(), stream)
        mime_data.setData(CustomTreeWidget.customMimeType, encoded)

        drag.setMimeData(mime_data)
        drag.exec_(supported_actions)

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        QTreeWidget.dropEvent(self, event)

    def fill_item(self, in_item, out_item):
        for col in range(in_item.columnCount()):
            for key in range(Qt.UserRole):
                role = Qt.ItemDataRole(key)
                out_item.setData(col, role, in_item.data(col, role))

    def fill_items(self, it_from, it_to):
        for ix in range(it_from.childCount()):
            it = QTreeWidgetItem(it_to)
            ch = it_from.child(ix)
            self.fill_item(ch, it)
            self.fill_items(ch, it)

    def encode_data(self, items, stream):
        stream.writeInt32(len(items))
        for item in items:
            p = item
            rows = []
            while p is not None:
                rows.append(self.indexFromItem(p).row())
                p = p.parent()
            stream.writeInt32(len(rows))
            for row in reversed(rows):
                stream.writeInt32(row)
        return stream

    def decode_data(self, encoded, tree):
        items = []
        rows = []
        stream = QDataStream(encoded, QIODevice.ReadOnly)
        while not stream.atEnd():
            n_items = stream.readInt32()
            for i in range(n_items):
                path = stream.readInt32()
                row = []
                for j in range(path):
                    row.append(stream.readInt32())
                rows.append(row)

        for row in rows:
            it = tree.topLevelItem(row[0])
            for ix in row[1:]:
                it = it.child(ix)
            items.append(it)
        return items
