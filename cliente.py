import sys
from PyQt4 import QtGui,QtCore, uic
from xmlrpclib import ServerProxy

class Interfaz_cliente(QtGui.QMainWindow):
    def __init__(self):
        super(Interfaz_cliente, self).__init__()
        uic.loadUi('cliente.ui', self)
        self.change_table()
        self.pushButton.clicked.connect(self.conect_server)
        self.pushButton_2.clicked.connect(self.begin)
        self.pushButton_2.clicked.connect(self.start_again)
        self.my_id = 0
        self.direction = 2
        self.in_game = False
        self.dead = False
        self.place = 0
        self.interval = 0
        self.timer= QtCore.QTimer(self)
        self.timer.timeout.connect(self.fill)
        self.timer.timeout.connect(self.play)
        self.timer.timeout.connect(self.check_time)
        self.timer.start(self.interval)
        self.show()
        self.server = None

    def fill(self):
        if self.in_game:
            game = self.server.game_status()
            self.tableWidget.setRowCount(game["tamY"])
            self.tableWidget.setColumnCount(game["tamX"])


    def check_time(self):
        if self.in_game:
            status = self.server.game_status()
            time = status["time"]
            if self.interval != time:
                self.interval = time
                self.timer.setInterval(self.time)

    def paint(self, sections, color):
        for section in sections:
            self.tableWidget.item(section[0], section[1]).setBackground(QtGui.QColor(color['r'], color['g'], color['b']))

    def conect_server(self):
        self.pushButton.setText("Pinging...")
        try:
            self.new_server()
            pong = self.server.ping()
            self.pushButton.setText("Pong!")
        except:
            self.pushButton.setText("No se pudo conectar")

    def new_server(self):
        self.url = self.lineEdit_3.text()
        self.port = self.spinBox.value()
        self.place = "http://" + self.url + ":" + str(self.port)
        self.server = ServerProxy(self.place)

    def play(self):
        if self.in_game:
            self.tableWidget.installEventFilter(self)
            status = self.server.game_status()
            snakes = status["snakes"]
            for snake in snakes:
                sections = snake["position"]
                color = snake["color"]
                self.paint(sections, color)

    def begin(self):
        try:
            self.new_server()
            player = self.server.new_player()
            self.lineEdit.setText(player["id"])
            self.my_id = player["id"]
            self.color = player["color"]
            self.red = self.color["r"]
            self.green = self.color["g"]
            self.blue = self.color["b"]
            self.lineEdit_2.setText("R:" + str(self.red) + " G:" + str(self.green) + " B:" + str(self.blue))
            self.lineEdit_2.setStyleSheet('QLineEdit {background-color: rgb('+str(self.red)+','+ str(self.green) + ',' + str(self.blue)+');}')
            self.in_game = True
        except:
            self.lineEdit.setText("No se pudo conectar al servidor")
            self.lineEdit_2.setText("Incorrect username or password.")


    def change_table(self):
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.tableWidget:
                key = event.key()
                if key == QtCore.Qt.Key_Up:
                    if self.direction != 2:
                        self.direction = 0
                elif key == QtCore.Qt.Key_Down:
                    if self.direction != 0:
                        self.direction = 2
                elif key == QtCore.Qt.Key_Right:
                    if self.direction != 3:
                        self.direction = 1
                elif key == QtCore.Qt.Key_Left:
                    if self.direction != 1:
                        self.direction = 3
                self.server.cambia_direction(self.my_id, self.direction)
        return QtGui.QMainWindow.eventFilter(self, source, event)

    def wasted(self):
        status = self.server.game_status()
        snakes = status["snakes"]
        for snake in snakes:
            if snake["id"] == self.my_id:
                return False
        self.dead = True
        return True

    def start_again(self):
        if self.dead:
            self.dead = False
            self.lineEdit.setText("")
            self.lineEdit.setText("")
            self.begin()
            self.timer.start()
            self.play()



servidor = QtGui.QApplication(sys.argv)
interfaz = Interfaz_cliente()
sys.exit(servidor.exec_())
