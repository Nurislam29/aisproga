import sys
import PyQt5
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QTime, QRect
from PyQt5.QtGui import QPainter, QColor
from random import choice, randint
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalDelegate
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, \
    QGraphicsOpacityEffect, QDialog, QMessageBox, QTableView, QDateEdit, QDateTimeEdit, QListWidgetItem, QListWidget, \
    QCalendarWidget
from PyQt5.QtGui import QPixmap
import sqlite3

conn = sqlite3.connect('planirovshik.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Plan(
Id INTEGER PRIMARY KEY AUTOINCREMENT,
Data varchar(30),
Time_start varchar(30),
Time_end varchar(30),
Job varchar(30),
Status_Job varchar(30))
""")
conn.commit()

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(410, 150, 1200, 750)
        self.setWindowTitle('Планировщик на день')
        self.spisokt = QLabel('Список дел', self)
        self.spisokt.setStyleSheet("font:18pt;")
        self.spisokt.adjustSize()
        self.spisokt.move(800, 30)

        self.datat = QLabel('Выберите дату:', self)
        self.datat.setStyleSheet("font:18pt; ")
        self.datat.adjustSize()
        self.datat.move(220, 80)

        self.image = QLabel(self)
        self.pixmap = QPixmap("1.jpg").scaled(1200, 700)
        self.image.resize(1200, 700)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.3)
        self.image.setGraphicsEffect(self.opacity_effect)
        self.image.setPixmap(self.pixmap)



        self.data = QCalendarWidget(self)
        self.data.setObjectName("Дата:")
        self.data.setStyleSheet("font:11pt;")
        self.data.move(50, 150)
        self.data.resize(500, 300)


        self.jobs = QListWidget(self)
        self.jobs.setGeometry(QRect(600, 100, 530, 400))
        self.jobs.setStyleSheet("font:14pt;")
        self.jobs.setObjectName("jobs")

        self.jobt = QLabel('Введите дело', self)
        self.jobt.setStyleSheet("font:15pt;")
        self.jobt.adjustSize()
        self.jobt.move(800, 510)
        self.job = QLineEdit(self)
        self.job.setObjectName("Дело")
        self.job.move(600, 550)
        self.job.resize(530, 40)
        self.job.setStyleSheet("font:12pt;")

        self.time_startt = QLabel('Время начала:', self)
        self.time_startt.move(100, 480)
        self.time_startt.setStyleSheet("font:12pt;")
        self.time_startt.adjustSize()
        self.time_start = QDateTimeEdit(QTime.currentTime(), self)
        self.time_start.setObjectName("Время начала")
        self.time_start.move(100, 510)
        self.time_start.resize(170, 40)
        self.time_start.setStyleSheet("font:12pt;")

        self.time_endt = QLabel('Время конца:', self)
        self.time_endt.move(320, 480)
        self.time_endt.setStyleSheet("font:12pt;")
        self.time_endt.adjustSize()
        self.time_end = QDateTimeEdit(QTime.currentTime(), self)
        self.time_end.setObjectName("Время конца")
        self.time_end.move(320, 510)
        self.time_end.resize(170, 40)
        self.time_end.setStyleSheet("font:12pt;")


        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("planirovshik.sqlite")
        self.db.open()
        self.view = QTableView(self)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('Plan')
        self.model.select()
        self.view.setModel(self.model)
        self.view.move(50, 60)
        self.view.resize(0, 0)

        cur.execute('''SELECT * from Plan ''')
        conn.commit()


        rows = self.model.rowCount()
        if not rows:
            return

        self.jobs.clear()

        cur.execute('''SELECT * from Plan ''')
        conn.commit()
        results = cur.fetchall()
        for result in results:
            item = QListWidgetItem(str(result[1] + '  ' + result[2] + '  ' + result[3] + '  ' + result[4]+'  '+result[5]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[5] == "Выполнено":
                item.setCheckState(QtCore.Qt.Checked)
                item.setBackground(QColor('#add9bc'))
            elif result[5] == "Не выполнено":
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setBackground(QColor('#f56973'))
            self.jobs.addItem(item)

        self.button_1 = QPushButton(self)
        self.button_1.move(650, 620)
        self.button_1.resize(170, 30)
        self.button_1.setText("Добавить дело")
        self.button_1.clicked.connect(self.run1)

        self.button_2 = QPushButton(self)
        self.button_2.move(900, 620)
        self.button_2.resize(170, 30)
        self.button_2.setText("Сохранить изменения")
        self.button_2.clicked.connect(self.run2)

        self.button_3 = QPushButton(self)
        self.button_3.move(750, 660)
        self.button_3.resize(170, 30)
        self.button_3.setText("Удалить дело")
        self.button_3.clicked.connect(self.run3)

    def run3(self):
        i = 0

        for item in self.jobs.selectedItems():
            sp = self.jobs.item(self.jobs.row(item)).text()
            text = sp.split("  ")
            d = text[0]
            ts = text[1]
            te = text[2]
            j = text[3]

            self.jobs.takeItem(self.jobs.row(item))

            print("Успешно удалено")
            msg = QMessageBox()
            msg.setWindowTitle("Успешно")
            msg.setText("Успешно удалено")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

        cur.execute('''DELETE from Plan WHERE Data = ? AND Time_start = ? AND Time_end=? AND Job=?''',
                (d, ts, te, j))
        conn.commit()

        self.w = Example()
        self.w.show()
        self.hide()

    def run1(self):
        conn = sqlite3.connect("planirovshik.sqlite")
        cur = conn.cursor()

        j = str(self.job.text())
        ts=str(self.time_start.text())
        te= str(self.time_end.text())
        d = self.data.selectedDate().toPyDate()

        cur.execute('''INSERT INTO Plan(Data, Time_start, Time_end,Job, Status_Job) VALUES (?, ?, ?,?,?)''',(d, ts, te, j, "Не выполнено"))
        conn.commit()

        msg = QMessageBox()
        msg.setWindowTitle("Успешно")
        msg.setText("Успешно добавлено")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.job.clear()

        self.w = Example()
        self.w.show()
        self.hide()

    def run2(self):
        conn = sqlite3.connect("planirovshik.sqlite")
        cur = conn.cursor()

        for i in range(self.jobs.count()):
            item = self.jobs.item(i)
            task = item.text()

            text=task.split("  ")
            d = text[0]
            ts = text[1]
            te = text[2]
            j=text[3]

            if item.checkState() == QtCore.Qt.Checked:
                #sj="Выполнено"
                cur.execute('''UPDATE Plan SET Status_Job = 'Выполнено' WHERE Data = ? AND Time_start = ? AND Time_end=? AND Job=?''',
                            (d,ts,te,j))
            else:
                #sj = "Не выполнено"
                cur.execute(
                    '''UPDATE Plan SET Status_Job = 'Не выполнено' WHERE Data = ? AND Time_start = ? AND Time_end=? AND Job=? ''',
                    (d, ts, te, j))

        conn.commit()

        messageBox = QMessageBox()
        messageBox.setText("Изменения сохранены")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

        self.w = Example()
        self.w.show()
        self.hide()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())