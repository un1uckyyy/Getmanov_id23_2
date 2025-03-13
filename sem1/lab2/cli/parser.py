import argparse


def init_parser() -> argparse.ArgumentParser:
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
