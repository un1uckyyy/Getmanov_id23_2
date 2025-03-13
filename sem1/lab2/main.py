from PyQt5.QtWidgets import QApplication

from cli.parser import init_parser
from widgets.widgets import DrawingArea


def main():
    parser = init_parser()
    args = parser.parse_args()

    app = QApplication([])
    window = DrawingArea(**args.__dict__)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
