import configparser
from game import *

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--who_first',type=str, default='AI')
    parser.add_argument('--board_size', type=int, default=15) #currently only 15by15 board png we have.
    parser.add_argument('--enable_ai', type=bool, default=True)
    parser.add_argument('--enable_second_ai', type=bool, default=False)
    args = parser.parse_args()

    # convert to dictionary
    params = vars(args)
    play(params)

if __name__ == "__main__":
    main()
