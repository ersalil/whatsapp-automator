from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
import pywhatkit
import sys

global file_path, ls
# ls = [8278687203, 9887997335, 8278686334, 7014336436, 8955641112]
from ui import Ui_MainWindow


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Whatsapp bulk by Salil Agrawal")
        self.show()
        self.ui.pushButton.clicked.connect(self.upload)
        self.ui.pushButton_2.clicked.connect(self.submit)

    def upload(self):
        global file_path
        fname = QFileDialog.getOpenFileName(self, 'Select the xlsx file')
        file_path = fname[0]
        self.ui.lineEdit.setText(file_path)

    def submit(self):
        global file_path, ls
        message = self.ui.plainTextEdit.toPlainText()
        wait_time = self.ui.spinBox.value()
        hour = self.ui.spinBox_2.value()
        minute = self.ui.spinBox_3.value()
        sheet_name = self.ui.lineEdit_2.text()
        if "" == sheet_name:
            df = pd.read_excel(file_path, sheet_name="Sheet1")
        else:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        ls = df['Numbers'].tolist()
        print("yes sch")
        self.worker = Work(ls, message, wait_time, hour, minute)
        self.worker.start()
        self.worker.progress_no.connect(self.progressbar)
        self.worker.current_no.connect(self.label_update)

    def label_update(self, no):
        print(no)
        self.ui.label.setText(f'Sending message to {no}')

    def progressbar(self, i):
        global ls
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue((i / len(ls)) * 100)


class Work(QThread):

    def __init__(self, ls2, message, waiting_time, hour, minute):
        QThread.__init__(self)
        self.hour = hour
        self.minute = minute
        self.ls = ls2
        self.message = message
        self.waiting_time = waiting_time

    current_no = pyqtSignal(str)
    progress_no = pyqtSignal(int)

    def run(self):
        i = 1
        now = datetime.now()
        print(self.hour, self.minute)

        if 0 == (int(self.hour) and int(self.minute)):
            h = int(now.strftime("%H"))
            m = int(now.strftime("%M")) + 2
            print("current time: ", h, ":", m)
        else:
            h = self.hour
            m = self.minute
        if 0 == self.waiting_time:
            self.waiting_time = 20

        for pno in [9413312301]:
            print(i, "Message to ", pno, " at ", h, m)
            str_no = str(pno)
            self.current_no.emit(str_no)
            pywhatkit.sendwhatmsg(f"+91{pno}", self.message, h, m, self.waiting_time)
            self.progress_no.emit(i)
            print("\n")
            i += 1
            if m == 59:
                h += 1
                m = 0
            else:
                m += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
