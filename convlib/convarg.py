from argparse import ArgumentParser

class Convarg(ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument("--input", required=True)
        self.add_argument("--impulse", required=True)
        self.add_argument("--out", required=True)
        self.parse_args()

