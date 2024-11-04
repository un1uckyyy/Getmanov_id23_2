import argparse

from PyQt5.QtWidgets import QApplication

from widgets.widgets import DrawingArea


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        help="file with program initial state"
    )
    parser.add_argument(
        "-c",
        "--create",
        default="random_initial_state.json",
        help="where the initial state will be saved"
    )

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    app = QApplication([])
    window = DrawingArea(**args.__dict__)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
