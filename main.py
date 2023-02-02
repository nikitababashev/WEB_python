import requests
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import os
from mapd import Ui_Form


WIDTH, HEIGHT = 600, 500


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ready.clicked.connect(self.createmaps)

    def createmaps(self):
        coords = self.coords.text().split()
        delta = self.delta.text()
        print(coords, delta)
        map_api_server = 'http://static-maps.yandex.ru/1.x/'
        map_params = {
            'll': ','.join(coords),
            'spn': ','.join([delta, delta]),
            'l': 'map'
        }
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print('Код ошибки:', response.status_code)
            sys.exit()

        self.map_file = 'map.png'
        with open(self.map_file, 'wb') as file:
            file.write(response.content)

        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setWindowTitle('Карта')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


app = QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec())