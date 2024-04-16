import sys
import os
import vlc
from PyQt5 import QtWidgets, QtGui, QtCore
from yt_dlp import YoutubeDL
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt, QPoint
import sqlite3

from channels_window import Ui_ChannelsWindow

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def create_database():
    # Подключаемся к базе данных (она будет создана, если еще не существует)
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()

    # Создаем таблицу каналов
    c.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')

    # Проверяем, есть ли уже записи в таблице
    c.execute('SELECT COUNT(*) FROM channels')
    if c.fetchone()[0] == 0:
        # Добавляем начальную запись, если таблица пуста
        c.execute('INSERT INTO channels (name, url) VALUES (?, ?)',
                  ("Rick Astley", "https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))

    # Закрываем подключение к базе данных
    conn.commit()
    conn.close()

create_database()

def get_channels():
    conn = sqlite3.connect('channels.db')
    c = conn.cursor()
    c.execute('SELECT * FROM channels')
    channels = c.fetchall()
    conn.close()
    return channels

class Player(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    state_changed = QtCore.pyqtSignal(str)
    signal_error = QtCore.pyqtSignal(str)  # Добавляем сигнал для ошибок

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent  # Сохраняем ссылку на родительский объект
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.reload_channels()

    def reload_channels(self):
        self.channels = get_channels()  # Загрузка каналов из базы данных
        if self.channels:
            self.current_channel_index = 0
            self.current_channel = self.channels[self.current_channel_index]
        else:
            self.current_channel = None  # Если нет каналов

        if self.parent:
            self.signal_error.connect(self.parent.show_toast)  # Подключаем сигнал к методу show_toast родителя

    def update_state(self, state):
        self.current_state = state
        self.state_changed.emit(state)

    def run(self):
        if self.current_channel:
            url = self.current_channel[2]  # URL текущего канала
            try:
                with YoutubeDL({'format': 'bestaudio'}) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    audio_url = info_dict.get('url', None)
                if audio_url:
                    self.player.set_media(self.instance.media_new(audio_url))
                    self.player.play()
                    self.update_state("Playing")
            except Exception as e:
                self.update_state("Error: " + str(e))
                print("Error playing:", e)
                self.signal_error.emit(str(e))  # Передаем ошибку в главное окно

    def stop(self):
        self.player.stop()
        self.update_state("Stopped")

class SystemTrayApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.player.state_changed.connect(self.update_tray_tooltip)
        self.player.signal_error.connect(self.show_toast)  # Подключаем обработку ошибок
        self.createTrayIcon()
        if not self.player.channels:  # Если нет каналов
            self.show_channels_window()  # Открыть окно управления каналами
        elif self.player.channels:  # Если каналы есть
            self.player.run()  # Начать воспроизведение

        # Установка стиля для Control Panel
        self.control_window = QtWidgets.QWidget()
        self.control_window.setWindowTitle("Control Panel")
        layout = QVBoxLayout()

        # Установить Control Panel как скрытое по умолчанию
        self.control_window.hide()

        # Создание кнопок управления
        buttons_layout = QHBoxLayout()
        button_size = QtCore.QSize(30, 30)

        buttons_css = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0);
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 50);
            }
        """

        # Создание метки для отображения названия канала
        self.channel_label = QLabel("" + self.player.current_channel[1])
        self.channel_label.setAlignment(Qt.AlignCenter)  # Центрирование текста
        self.channel_label.setStyleSheet("""
                    QLabel {
                        font-size: 14pt;
                        color: white;
                        background-color: rgba(0, 0, 0, 150);
                        padding: 5px;
                        border-radius: 10px;
                    }
                """)
        layout.addWidget(self.channel_label)

        self.previous_button = QPushButton()
        self.previous_button.setIcon(QtGui.QIcon(resource_path("left.png")))
        self.previous_button.setIconSize(button_size)
        self.previous_button.setMinimumSize(button_size)
        self.previous_button.clicked.connect(self.play_previous_channel)
        self.previous_button.setStyleSheet(buttons_css)

        self.play_button = QPushButton()
        self.play_button.setIcon(QtGui.QIcon(resource_path("play.png")))
        self.play_button.setIconSize(button_size)
        self.play_button.setMinimumSize(button_size)
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setStyleSheet(buttons_css)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(QtGui.QIcon(resource_path("stop.png")))
        self.stop_button.setIconSize(button_size)
        self.stop_button.setMinimumSize(button_size)
        self.stop_button.clicked.connect(self.player.stop)
        self.stop_button.setStyleSheet(buttons_css)

        self.next_button = QPushButton()
        self.next_button.setIcon(QtGui.QIcon(resource_path("right.png")))
        self.next_button.setIconSize(button_size)
        self.next_button.setMinimumSize(button_size)
        self.next_button.clicked.connect(self.play_next_channel)
        self.next_button.setStyleSheet(buttons_css)

        # Добавление кнопок в горизонтальный макет
        buttons_layout.addWidget(self.previous_button)
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addWidget(self.next_button)

        # Создание слайдера громкости
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.player.player.audio_get_volume())
        self.volume_slider.valueChanged.connect(self.player.player.audio_set_volume)

        layout.addLayout(buttons_layout)
        layout.addWidget(self.volume_slider)

        self.control_window.setLayout(layout)
        self.control_window.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint | QtCore.Qt.NoDropShadowWindowHint)
        self.control_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def update_tray_tooltip(self, state):
        if state == "Playing":
            icon_path = resource_path("green_circle.png")
        else:
            icon_path = resource_path("red_circle.png")
        self.tray_icon.setIcon(QtGui.QIcon(icon_path))
        self.tray_icon.setToolTip(state)

    def createTrayIcon(self):
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        icon_path = resource_path("design.png")  # Убедитесь, что файл действительно существует по этому пути
        self.tray_icon.setIcon(QtGui.QIcon(icon_path))
        self.tray_icon.setToolTip("Stopped")

        # Создание контекстного меню для иконки в трее
        tray_menu = QtWidgets.QMenu()

        quit_action = QtWidgets.QAction("Exit", self)
        quit_action.triggered.connect(QtWidgets.qApp.quit)

        channels_action = tray_menu.addAction("Каналы")
        channels_action.triggered.connect(self.show_channels_window)  # Подключение сигнала к слоту

        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Включаем обработку клика по иконке
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Показываем иконку
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        self.player.reload_channels()  # Перезагрузка каналов перед показом окна
        if reason   == QtWidgets.QSystemTrayIcon.Trigger:
            pos = QtGui.QCursor.pos()
            self.control_window.move(pos.x() - self.control_window.width() // 2, pos.y() - self.control_window.height())
            self.control_window.show()

    def play_previous_channel(self):
        self.player.current_channel_index = (self.player.current_channel_index - 1) % len(self.player.channels)
        self.player.current_channel = self.player.channels[self.player.current_channel_index]
        self.channel_label.setText(self.player.current_channel[1])
        # Убираем вызов self.player.run()

    def toggle_playback(self):
        if self.player.current_state in ["Stopped", "Paused"]:
            self.player.run()  # Corrected, no arguments passed
        else:
            self.player.player.pause()
            self.player.update_state("Paused")
            self.player.run()

    def play_next_channel(self):
        self.player.current_channel_index = (self.player.current_channel_index + 1) % len(self.player.channels)
        self.player.current_channel = self.player.channels[self.player.current_channel_index]
        self.channel_label.setText(self.player.current_channel[1])
        # Убираем вызов self.player.run()

    def show_channels_window(self):
        self.channels_window = QtWidgets.QDialog()  # Создаем экземпляр QDialog
        self.ui_channels = Ui_ChannelsWindow(self.channels_window)  # Передаем этот экземпляр в Ui_ChannelsWindow
        self.channels_window.show()  # Показываем окно

    def show_toast(self, message, duration=3000):
        if not hasattr(self, 'toast_label'):
            self.toast_label = QLabel(self.control_window)
            self.toast_label.setStyleSheet("""
                background-color: rgba(0, 0, 0, 180);
                color: white;
                padding: 8px;
                border-radius: 10px;
                font-size: 12pt;
            """)
            self.toast_label.setAlignment(Qt.AlignCenter)
            self.toast_label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.toast_label.setText(message)
        self.toast_label.adjustSize()  # Adjust size to fit the text
        self.toast_label.move(
            self.control_window.geometry().center() - self.toast_label.rect().center() - QPoint(0,
                                                                                                self.control_window.height() // 2)
        )
        self.toast_label.show()
        QtCore.QTimer.singleShot(duration, self.toast_label.hide)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Это предотвратит закрытие приложения при закрытии всех окон
    w = SystemTrayApp()
    sys.exit(app.exec_())