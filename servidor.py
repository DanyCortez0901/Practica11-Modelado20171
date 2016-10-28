# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore, uic
from random import randint
from SimpleXMLRPCServer import SimpleXMLRPCServer
import uuid

class Snake():
    def __init__(self):
        self.id = str(uuid.uuid4())[:8]
        red, green, blue = randint(0,255), randint(0,255), randint(0,255)
        self.color = {"r": red, "g": green, "b": blue}
        self.position = []
        self.sections = []
        self.direction = "Down"
        self.score = 0

    def get_attributes(self):
        return {
            'id': self.id,
            'position': self.position,
            'color': self.color
        }
class Interfaz_server(QtGui.QMainWindow):

    def __init__(self):
        super(Interfaz_server, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.snakes = []
        self.pushButton_3.hide()
        self.start = False
        self.pausa = False
        self.timer = None
        self.time_spawn_points = None
        self.time_points = None
        self.Score = 0
        self.points = []
        self.change_table()
        self.fill()
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.pushButton.clicked.connect(self.server_on)
        self.spinBox.valueChanged.connect(self.update_timer)
        self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)
        self.spinBox_2.valueChanged.connect(self.update)
        self.pushButton_2.clicked.connect(self.start_game)
        self.spinBox_3.valueChanged.connect(self.update)
        self.pushButton_3.clicked.connect(self.end_game)
        self.show()

    def update_snakes(self):
        for snake in self.snakes:
            snake.position = []
            for section in snake.sections:
                snake.position.append((section[0], section[1]))

    def start_game(self):
        if not self.start:
            self.new_snake()
            self.paint_snakes()
            self.pushButton_2.setText("Stop")
            self.pushButton_3.show()
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.move_snakes)
            self.time_points = QtCore.QTimer(self)
            self.delet_points = QtCore.QTimer(self)
            self.time_spawn_points = QtCore.QTimer(self)
            self.time_spawn_points.timeout.connect(self.eat)
            self.time_spawn_points.start(100)
            self.time_points.timeout.connect(self.new_point)
            self.time_points.start(2000)
            self.delet_points.timeout.connect(self.erase_point)
            self.delet_points.start(3850)
            self.timer.start(100)
            self.timer_position = QtCore.QTimer(self)
            self.timer_position.timeout.connect(self.update_snakes)
            self.timer_position.start(100)
            self.tableWidget.installEventFilter(self)
            self.start = True
        elif self.start and not self.pausa:
            self.timer.stop()
            self.time_points.stop()
            self.time_spawn_points.stop()
            self.pausa = True
            self.pushButton_2.setText("Reanudar el Juego")
        elif self.pausa:
            self.timer.start()
            self.time_points.start()
            self.time_spawn_points.start()
            self.pausa = False
            self.pushButton_2.setText("Stop")

    def end_game(self):
        self.snakes = []
        self.timer.stop()
        self.points = []
        self.Score = 0
        self.time_spawn_points.stop()
        self.time_points.stop()
        self.start = False
        self.pushButton_2.setText("Play")
        self.pushButton_3.hide()
        self.fill()

    def status(self):
        self.servidor.handle_request()

    def server_on(self):
        puerto = self.spinBox_4.value()
        direction = self.lineEdit.text()
        self.servidor = SimpleXMLRPCServer((direction, 0))
        puerto = self.servidor.server_address[1]
        self.spinBox_4.setValue(puerto)
        self.spinBox_4.setReadOnly(True)
        self.lineEdit.setReadOnly(True)
        self.pushButton.setEnabled(False)
        self.servidor.register_function(self.ping)
        self.servidor.register_function(self.new_player)
        self.servidor.register_function(self.server_change)
        self.servidor.register_function(self.game_status)
        self.servidor.timeout = 0
        self.timer_s = QtCore.QTimer(self)
        self.timer_s.timeout.connect(self.status)
        self.timer_s.start(self.servidor.timeout)

    def server_change(self, id_, direction):
        for snake in self.snakes:
            if snake.id == id_:
                if direction == 0:
                    if snake.direction is not "Down":
                        snake.direction = "Up"
                if numero == 1:
                    if snake.direction is not "left":
                        snake.direction = "Right"
                if numero == 2:
                    if snake.direction is not "Up":
                        snake.direction = "Down"
                if numero == 3:
                    if snake.direction is not "Right":
                        snake.direction = "Left"
        return True


    def game_status(self):
        return {'time': self.servidor.timeout, 'tamX': self.tableWidget.columnCount(),
            'tamY': self.tableWidget.rowCount(), 'snakes': self.get_snakes()}


    def get_snakes(self):
        get = list()
        for snake in self.snakes:
            get.append(snake.get_attributes())
        return get

    def new_player(self):
        new = new_snake()
        attributes = {"id": new.id, "color": new.color}
        return attributes

    def new_snake(self):
        new = Snake()
        good_posittion = False
        while not good_posittion:
            good_posittion = True
            i = randint(1, self.tableWidget.rowCount()/2)
            j = randint(1, self.tableWidget.columnCount()-1)
            head = [i,j]
            stomach = [i + 1, j]
            tail = [i + 2, j]
            for snake in self.snakes:
                if head in snake.sections or stomach in snake.sections or tail in snake.sections:
                    good_posittion = False
                    break
            new.sections = [head, stomach, tail]
            self.snakes.append(new)
            return new

    def ping(self):
        return "¡Pong!"
    def update_timeout(self):
        self.servidor.timeout = self.time.value()
        self.timer_s.setInterval(self.time.value())

    def update_timer(self):
        valor = self.spinBox.value()
        self.timer.setInterval(valor)

    def fill(self):
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
                self.tableWidget.item(i,j).setBackground(QtGui.QColor(251,251,251))

    def change_table(self):
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def update(self):
        self.tableWidget.setColumnCount(self.spinBox_2.value())
        self.tableWidget.setRowCount(self.spinBox_3.value())
        self.fill()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress and source is self.tableWidget:
                direction = event.key()
                snake = self.snakes[0]
                if direction == QtCore.Qt.Key_Up:
                    if snake.direction is not "Down":
                        snake.direction = "Up"
                elif direction == QtCore.Qt.Key_Down:
                    if snake.direction is not "Up":
                        snake.direction = "Down"
                elif direction == QtCore.Qt.Key_Right:
                    if snake.direction is not "Left":
                        snake.direction = "Right"
                elif direction == QtCore.Qt.Key_Left:
                    if snake.direction is not "Right":
                        snake.direction = "Left"
        return QtGui.QMainWindow.eventFilter(self, source, event)

    def paint_snakes(self):
        snake = self.snakes[0]
        for box in snake.sections:
            self.tableWidget.item(box[0], box[1]).setBackground(QtGui.QColor(snake.color["r"], snake.color["g"], snake.color["b"]))

    def erase_point(self):
        if self.points != []:
            point = self.points.pop(0)
            i = point[0]
            j = point[1]
            self.tableWidget.item(i,j).setBackground(QtGui.QColor(251,251,251))
        return

    def new_point(self):
        i = randint(0, self.tableWidget.rowCount()-1)
        j = randint(0, self.tableWidget.columnCount()-1)
        for snake in self.snakes:
            if [i,j] in snake.position:
                break
        self.points.append([i,j])
        self.tableWidget.item(i,j).setBackground(QtGui.QColor(0,0,0))

    def eat(self):
        for snake in self.snakes:
            for point in self.points:
                if snake.position[-1][0] == point[0] and snake.position[-1][1] == point[1]:
                    snake.score += 1
                    snake.sections.append([point[0],point[1]])
                    self.points.remove(point)
                    self.paint_snakes()
                    return True
        return False

    def crash(self, snake):
        for box in snake.position[0:len(snake.position)-2]:
            if snake.position[-1][0] == box[0] and snake.position[-1][1] == box[1]:
                return True
        return False

    def move_snakes(self):
        for snake in self.snakes:
            if self.crash(snake):
                self.snakes.remove(snake)
                self.fill()
                s = self.new_snake()
                self.snakes = [s]
            self.tableWidget.item(snake.sections[0][0],snake.sections[0][1]).setBackground(QtGui.QColor(251,251,251))
            i = 0
            for box in snake.sections[0: len(snake.position)-1]:
                i += 1
                box[0] = snake.sections[i][0]
                box[1] = snake.sections[i][1]

            rows = self.tableWidget.rowCount()
            columns =  self.tableWidget.columnCount()
            if snake.direction is "Down":
                if snake.sections[-1][0] + 1 < rows:
                    snake.sections[-1][0] += 1
                else:
                    snake.sections[-1][0] = 0
            if snake.direction is "Right":
                if snake.sections[-1][1] + 1 < columns:
                    snake.sections[-1][1] += 1
                else:
                    snake.sections[-1][1] = 0
            if snake.direction is "Up":
                if snake.sections[-1][0] != 0:
                    snake.sections[-1][0] -= 1
                else:
                    snake.sections[-1][0] = rows-1
            if snake.direction is "Left":
                if snake.sections[-1][1] != 0:
                    snake.sections[-1][1] -= 1
                else:
                    snake.sections[-1][1] = columns-1
        self.paint_snakes()


servidor = QtGui.QApplication(sys.argv)
interfaz = Interfaz_server()
sys.exit(servidor.exec_())
