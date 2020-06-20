import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtCore import Qt


class ScreenWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(150)

        style = """
            font-size: 30px;
        """
        self.setStyleSheet(style)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.expression = QLabel("")
        self.expression.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.expression)

        self.result = QLabel("0")
        self.result.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.result)

    def update_expression(self, new_expr):
        self.expression.setText(new_expr)

    def update_result(self, result):
        self.result.setText(str(result))


class Button(QPushButton):
    def __init__(self, text, callback, bg_color, custom_mark=None):
        super().__init__()
        self.setText(text)
        if not custom_mark:
            self.clicked.connect(lambda e: callback(e, text))
        else:
            self.clicked.connect(lambda e: callback(e, custom_mark))
        style = f"""
            background-color: rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]});
            border: none;
            height:70px
        """
        style_hover = f"""
            background-color: rgb({bg_color[0]-10}, {bg_color[1]-10}, {bg_color[2]-10});
        """
        s = "QPushButton {" + style + "}" + "QPushButton:hover {" + style_hover + "}"
        self.setStyleSheet(s)


class ButtonsGrid(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        c1 = (175, 175, 175)
        c2 = (220, 220, 220)
        c3 = (250, 250, 250)
        buttons = [
            Button("CE", self.parent.clear_exp, c2),
            Button("C", self.parent.clear, c2),
            Button("<", self.parent.del_last, c2),
            Button("/", self.parent.add_to_exp, c2),

            Button("7", self.parent.add_to_exp, c3),
            Button("8", self.parent.add_to_exp, c3),
            Button("9", self.parent.add_to_exp, c3),
            Button("x", self.parent.add_to_exp, c2, custom_mark="*"),

            Button("4", self.parent.add_to_exp, c3),
            Button("5", self.parent.add_to_exp, c3),
            Button("6", self.parent.add_to_exp, c3),
            Button("-", self.parent.add_to_exp, c2),

            Button("1", self.parent.add_to_exp, c3),
            Button("2", self.parent.add_to_exp, c3),
            Button("3", self.parent.add_to_exp, c3),
            Button("+", self.parent.add_to_exp, c2),

            Button("+/-", self.parent.change_sign, c3),
            Button("0", self.parent.add_to_exp, c3),
            Button(",", self.parent.add_to_exp, c3, custom_mark="."),
            Button("=", self.parent.calc, c1),
        ]
        h_layout = QHBoxLayout()
        self.layout.addLayout(h_layout)
        for i, b in enumerate(buttons):
            h_layout.addWidget(b)
            if (i + 1) % 4 == 0:
                h_layout = QHBoxLayout()
                self.layout.addLayout(h_layout)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.grabKeyboard()
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        self.screen = ScreenWidget()
        self.v_layout.addWidget(self.screen)

        self.buttons = ButtonsGrid(self)
        self.v_layout.addWidget(self.buttons)
        self.v_layout.addStretch()

        self.exp = ""
        self.res = 0
        self.sign = 1

    def keyPressEvent(self, event):
        keys_digits = [
            Qt.Key_0, Qt.Key_1, Qt.Key_2,
            Qt.Key_3, Qt.Key_4, Qt.Key_5,
            Qt.Key_6, Qt.Key_7, Qt.Key_8,
            Qt.Key_9,
        ]
        keys_signs = [
            Qt.Key_Asterisk, Qt.Key_Slash,
            Qt.Key_Plus, Qt.Key_Minus, Qt.Key_Comma,
        ]
        keys_calc = [
            Qt.Key_Enter, Qt.Key_Return, Qt.Key_Equal
        ]
        del_keys = [
            Qt.Key_Backspace
        ]
        if event.key() in keys_digits + keys_signs:
            self.add_to_exp(None, event.text())
        elif event.key() in keys_calc:
            self.calc(None, None)
        elif event.key() in del_keys:
            self.del_last(None, None)

    def add_to_exp(self, event, mark):
        keys_signs = ['+', '-', '/', '*', '.']
        if mark in keys_signs:
            if len(self.exp) != 0:
                if self.exp[-1] in ['+', '-', '*', '/', '.']:
                    self.exp = self.exp[:-1] + mark
                else:
                    self.exp += mark
                self.screen.update_expression(self.exp)
            else:
                if mark == '-':
                    self.exp += mark
                    self.screen.update_expression(self.exp)
        else:
            self.exp += mark
            self.screen.update_expression(self.exp)

    def calc(self, *args, **kwargs):
        if len(self.exp) > 0:
            if self.exp[-1] in ['+', '-', '*', '/', '.']:
                exp = self.exp[:-1]
            else:
                exp = self.exp
            try:
                self.res = eval(exp)
            except ZeroDivisionError:
                self.res = 0
        else:
            self.res = 0
        self.screen.update_result(self.res * self.sign)

    def clear(self, event, mark):
        self.exp = ""
        self.res = 0
        self.sign = 1
        self.screen.update_expression(self.exp)
        self.screen.update_result(self.res * self.sign)

    def clear_exp(self, event, mark):
        self.exp = ""
        self.screen.update_expression(self.exp)

    def del_last(self, event, mark):
        self.exp = self.exp[:-1]
        self.screen.update_expression(self.exp)

    def change_sign(self, event, mark):
        self.sign = -1 if self.sign == 1 else 1
        self.screen.update_result(self.res * self.sign)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumHeight(500)
        self.setMinimumWidth(400)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        self.widget = MainWidget()
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.resize(400, 500)
    window.show()

    sys.exit(app.exec_())
