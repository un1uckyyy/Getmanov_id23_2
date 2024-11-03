from PyQt5.QtWidgets import QApplication

from widgets.widgets import DrawingArea


def main():
    app = QApplication([])
    window = DrawingArea()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
