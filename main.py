from omok.game import *


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', type=int, default=15)
    parser.add_argument('--enable_ai', type=bool, default=True)
    parser.add_argument('--enable_second_ai', type=bool, default=False)

    args = parser.parse_args()

    # convert to dictionary
    params = vars(args)
    play(params)


if __name__ == "__main__":
    main()
