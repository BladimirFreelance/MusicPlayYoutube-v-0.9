import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChannelsWindow(object):

    def __init__(self, ChannelsWindow):
        self.URLLabel = None
        self.URLEditLine = None
        self.NamEditLine = None
        self.NameLabel = None
        self.MinuspushButton = None
        self.PluspushButton = None
        self.treeWidgetElementChanal = None
        self.buttonBox = None
        self.current_channel_id = None  # ID текущего выбранного канала
        self.ChannelsWindow = ChannelsWindow
        self.setupUi(ChannelsWindow)
        self.load_channels()
        self.channel_added = False

    def setupUi(self, ChannelsWindow):
        ChannelsWindow.setObjectName("ChannelsWindow")
        ChannelsWindow.resize(1280, 900)
        ChannelsWindow.setMaximumSize(QtCore.QSize(1280, 900))
        ChannelsWindow.setStyleSheet("background-color: #2b2d30")
        self.gridLayout = QtWidgets.QGridLayout(ChannelsWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(ChannelsWindow)
        self.buttonBox.setMinimumSize(QtCore.QSize(206, 0))
        self.buttonBox.setStyleSheet(
            "color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;")
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.add_channel_to_db_and_close)
        self.buttonBox.rejected.connect(ChannelsWindow.close)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.add_channel_to_db)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.frame = QtWidgets.QFrame(ChannelsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_9 = QtWidgets.QFrame(self.frame_3)
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout.addWidget(self.frame_9)
        self.Namelabel = QtWidgets.QLabel(self.frame_3)
        self.Namelabel.setMinimumSize(QtCore.QSize(222, 0))
        self.Namelabel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.Namelabel.setStyleSheet(
            "color: white;border-style: outset; font: bold 16px; min-width: 10em; padding: 6px;")
        self.Namelabel.setObjectName("Namelabel")
        self.verticalLayout.addWidget(self.Namelabel)
        self.frame_8 = QtWidgets.QFrame(self.frame_3)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout.addWidget(self.frame_8)
        self.URLLabel = QtWidgets.QLabel(self.frame_3)
        self.URLLabel.setMinimumSize(QtCore.QSize(222, 0))
        self.URLLabel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.URLLabel.setStyleSheet(
            "color: white;border-style: outset; font: bold 16px; min-width: 10em; padding: 6px;")
        self.URLLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.URLLabel.setObjectName("URLLabel")
        self.verticalLayout.addWidget(self.URLLabel)
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout.addWidget(self.frame_10)
        self.frame_9.raise_()
        self.frame_8.raise_()
        self.Namelabel.raise_()
        self.frame_10.raise_()
        self.URLLabel.raise_()
        self.gridLayout_3.addWidget(self.frame_3, 1, 2, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(900, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_2.addWidget(self.frame_6)
        self.NamEditLine = QtWidgets.QLineEdit(self.frame_4)
        self.NamEditLine.setMinimumSize(QtCore.QSize(206, 0))
        self.NamEditLine.setStyleSheet(
            "color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;")
        self.NamEditLine.setObjectName("NamEditLine")
        self.verticalLayout_2.addWidget(self.NamEditLine)
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_2.addWidget(self.frame_7)
        self.URLEditLine = QtWidgets.QLineEdit(self.frame_4)
        self.URLEditLine.setMinimumSize(QtCore.QSize(206, 0))
        self.URLEditLine.setStyleSheet(
            "color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;")
        self.URLEditLine.setObjectName("URLEditLine")
        self.verticalLayout_2.addWidget(self.URLEditLine)
        self.frame_11 = QtWidgets.QFrame(self.frame_4)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_2.addWidget(self.frame_11)
        self.gridLayout_3.addWidget(self.frame_4, 1, 3, 1, 1)
        self.knopkiplusminus = QtWidgets.QFrame(self.frame)
        self.knopkiplusminus.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.knopkiplusminus.setFrameShadow(QtWidgets.QFrame.Raised)
        self.knopkiplusminus.setObjectName("knopkiplusminus")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.knopkiplusminus)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_5 = QtWidgets.QFrame(self.knopkiplusminus)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout.addWidget(self.frame_5)
        self.PluspushButton = QtWidgets.QPushButton(self.knopkiplusminus)
        self.PluspushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.PluspushButton.setMaximumSize(QtCore.QSize(40, 40))
        self.PluspushButton.setStyleSheet("color: white; font: bold 40px; border-style: outset;")
        self.PluspushButton.setObjectName("PluspushButton")

        self.PluspushButton.clicked.connect(self.add_new_channel_ui)

        self.horizontalLayout.addWidget(self.PluspushButton)
        self.MinuspushButton = QtWidgets.QPushButton(self.knopkiplusminus)
        self.MinuspushButton.setEnabled(True)
        self.MinuspushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.MinuspushButton.setMaximumSize(QtCore.QSize(40, 40))
        self.MinuspushButton.setMouseTracking(False)
        self.MinuspushButton.setTabletTracking(False)
        self.MinuspushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.MinuspushButton.setStyleSheet("color: white; font: bold 40px;border-style: outset;")
        self.MinuspushButton.setAutoRepeatDelay(40)
        self.MinuspushButton.setAutoRepeatInterval(40)
        self.MinuspushButton.setAutoDefault(True)
        self.MinuspushButton.setObjectName("MinuspushButton")
        self.horizontalLayout.addWidget(self.MinuspushButton)

        self.MinuspushButton.clicked.connect(self.delete_selected_channel)  # Подключаем слот удаления к кнопке "-"

        self.gridLayout_3.addWidget(self.knopkiplusminus, 0, 0, 1, 1)

        self.treeWidgetElementChanal = QtWidgets.QTreeWidget(self.frame)

        self.treeWidgetElementChanal.setMinimumSize(QtCore.QSize(206, 0))
        self.treeWidgetElementChanal.setMaximumSize(QtCore.QSize(400, 780))

        self.treeWidgetElementChanal.setHeaderHidden(True)  # Скрывает заголовок колонки

        self.treeWidgetElementChanal.setStyleSheet(
            "color: white;border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;")
        self.treeWidgetElementChanal.setObjectName("treeWidgetElementChanal")

        self.treeWidgetElementChanal.itemClicked.connect(self.on_channel_selected)

        self.gridLayout_3.addWidget(self.treeWidgetElementChanal, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(30, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3.addWidget(self.frame_2, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.retranslateUi(ChannelsWindow)
        QtCore.QMetaObject.connectSlotsByName(ChannelsWindow)

    def retranslateUi(self, ChannelsWindow):
        _translate = QtCore.QCoreApplication.translate
        ChannelsWindow.setWindowTitle(_translate("ChannelsWindow", "ChannelsWindow"))
        self.Namelabel.setText(_translate("ChannelsWindow", "Name:"))
        self.URLLabel.setText(_translate("ChannelsWindow", "URL:"))
        self.PluspushButton.setText(_translate("ChannelsWindow", "+"))
        self.MinuspushButton.setText(_translate("ChannelsWindow", "-"))

    def load_channels(self):
        conn = sqlite3.connect('channels.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, url FROM channels")
        channels = cursor.fetchall()
        conn.close()

        # Очистка текущих элементов дерева, если они есть
        self.treeWidgetElementChanal.clear()

        # Добавление каналов в QTreeWidget
        for channel in channels:
            channel_id, name, url = channel
            item = QtWidgets.QTreeWidgetItem(self.treeWidgetElementChanal)
            item.setText(0, name)
            item.setData(0, QtCore.Qt.UserRole, channel_id)  # Сохраняем ID канала как данные элемента

    # Функция добавления нового пустого элемента в UI для редактирования
    def add_new_channel_ui(self):
        new_item = QtWidgets.QTreeWidgetItem(self.treeWidgetElementChanal)
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)
        self.treeWidgetElementChanal.setCurrentItem(new_item)
        self.treeWidgetElementChanal.editItem(new_item, 0)
        # Очистка полей
        self.NamEditLine.clear()
        self.URLEditLine.clear()

        self.NamEditLine.setFocus()  # Устанавливаем фокус на NamEditLine

    # Удаление канала
    def delete_selected_channel(self):
        current_item = self.treeWidgetElementChanal.currentItem()
        if current_item is not None:
            current_channel_id = current_item.data(0, QtCore.Qt.UserRole)
            if current_channel_id:
                # Создание и стилизация диалогового окна подтверждения
                msg_box = QtWidgets.QMessageBox(self.ChannelsWindow)
                msg_box.setIcon(QtWidgets.QMessageBox.Question)
                msg_box.setAutoFillBackground(False)
                msg_box.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.CustomizeWindowHint)
                msg_box.setStyleSheet(
                    "color: white; border-style: outset; font: bold 20px; padding: 10px;")
                msg_box.setWindowTitle('Подтверждение')
                msg_box.setText("Вы уверены, что хотите удалить выбранный канал?")
                msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
                reply = msg_box.exec_()

                if reply == QtWidgets.QMessageBox.Yes:
                    # Удаление канала из базы данных
                    conn = sqlite3.connect('channels.db')
                    c = conn.cursor()
                    c.execute("DELETE FROM channels WHERE id=?", (current_channel_id,))
                    conn.commit()
                    conn.close()

                    # Обновление списка каналов
                    self.load_channels()

    #Просмотр информации каналов
    def on_channel_selected(self, item, column):
        self.NamEditLine.setText(item.text(0))  # Channel name
        self.current_channel_id = item.data(0, QtCore.Qt.UserRole)  # Channel ID
        # Load URL from the database
        conn = sqlite3.connect('channels.db')
        c = conn.cursor()
        c.execute("SELECT url FROM channels WHERE id=?", (self.current_channel_id,))
        url = c.fetchone()
        if url:
            self.URLEditLine.setText(url[0])
        conn.close()

    # Общее окно предупреждений
    def show_warning(self, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.CustomizeWindowHint)
        msg_box.setText(message)
        msg_box.setStyleSheet(
            "background-color: #2b2d30; color: white; border-style: outset; border-color: beige; font: bold 20px; padding: 10px;")
        msg_box.setWindowTitle("Warning")
        msg_box.exec_()

    # Кнопки OK, Cancel, Apply

    def add_channel_to_db_and_close(self): # Конпка Ok
        self.add_channel_to_db()
        # Если канал успешно добавлен, закрыть окно
        if self.channel_added:
            self.ChannelsWindow.hide()

    def add_channel_to_db(self): # Функция добавления канала в базу данных
        name = self.NamEditLine.text().strip()
        url = self.URLEditLine.text().strip()
        if not name or not url:
            # Отобразить предупреждение
            self.show_warning("Необходимо указать Name-имя и URL-адрес")
            return

        try:
            # Подключаемся к базе данных и вставляем новый канал
            conn = sqlite3.connect('channels.db')
            c = conn.cursor()
            if self.current_channel_id:
                c.execute("UPDATE channels SET name=?, url=? WHERE id=?", (name, url, self.current_channel_id))
            else:
                c.execute("INSERT INTO channels (name, url) VALUES (?, ?)", (name, url))
            conn.commit()
        except sqlite3.Error as e:
            self.show_warning(f"Database error: {e}")
        finally:
            conn.close()
            self.channel_added = True  # Установить флаг, если канал был добавлен
            self.load_channels()  # Обновить список каналов
            self.current_channel_id = None  # Reset the current channel ID


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChannelsWindow = QtWidgets.QDialog()
    # ui = Ui_ChannelsWindow()
    ui = Ui_ChannelsWindow(ChannelsWindow)  # Передайте экземпляр в класс
    ChannelsWindow.show()
    app.exec_()