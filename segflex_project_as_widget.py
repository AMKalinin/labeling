from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import segflex_seg_window as seg_window

"""
class project_as_widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
"""

class project_as_widget(QGroupBox):
    Signal_OneParameter = pyqtSignal(str)

    def __init__(self,
                 name,
                 classes,
                 last_change,
                 creator,
                 creation_time,
                 parent=None,
                 ide=0):
        #QGroupBox.__init__(self, name, classes, parent, ide)
        super().__init__()

        layout = QHBoxLayout()
        layout_preview = QVBoxLayout()
        layout_info = QVBoxLayout()
        layout_status = QVBoxLayout()
        layout_jobs = QVBoxLayout()
        layout_actions =QVBoxLayout()

        layout.addLayout(layout_preview)
        layout.addLayout(layout_info)
        layout.addLayout(layout_status)
        layout.addLayout(layout_jobs)
        layout.addLayout(layout_actions)


        image = QLabel(self)
        pixmap = QtGui.QPixmap("image.jpg")
        image.setPixmap(pixmap)
        image.setFixedSize(100, 100)

        info_number = QLabel("#" + str(ide) + ' ' + name)
        info_created_by = QLabel("Created by " + creator + "on " + creation_time)
        info_last_update = QLabel("Last updated: " + last_change)

        status = QLabel(" ".join(str(classes)))

        jobs = QLabel("0 of 1 jobs")

        self.btn_open = QPushButton("Open")

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.emit_delete_signal)
        self.btn_edit = QPushButton("Edit")
        self.btn_edit.clicked.connect(self.on_edit)
        actions_bar = QComboBox()
        actions_bar.addItems(["do smth1", "do smth2"])

        btn_id_in_layout = QPushButton("print id")
        #btn_id_in_layout.clicked.connect()


        layout_preview.addWidget(image)
        layout_info.addWidget(info_number)
        layout_info.addWidget(info_created_by)
        layout_info.addWidget(info_last_update)
        layout_status.addWidget(status)
        layout_jobs.addWidget(jobs)
        layout_actions.addWidget(self.btn_open)

        layout_actions.addWidget(self.btn_delete)
        layout_actions.addWidget(self.btn_edit)

        layout_actions.addWidget(actions_bar)


        self.setMaximumHeight(120)
        self.setLayout(layout)

    def emit_delete_signal(self):
        #self.Signal_OneParameter.emit("date_str")
        self.deleteLater()

    def on_edit(self):
        self.seg_window = seg_window.seg_window(self)
        self.seg_window.exec_()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = project_as_widget()
    w.show()
    sys.exit(app.exec_())

