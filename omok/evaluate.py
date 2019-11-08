from omok.boardstate import *

WHITE_6PATTERNS = [['empty', 'white', 'white', 'white', 'white','empty'],
                   ['empty', 'white', 'white', 'white', 'empty','empty'],
                   ['empty', 'empty', 'white', 'white', 'white','empty'],
                   ['empty', 'white', 'white', 'empty', 'white','empty'],
                   ['empty', 'white', 'empty', 'white', 'white','empty'],
                   ['empty', 'empty', 'white', 'white', 'empty','empty'],
                   ['empty', 'empty', 'white', 'empty', 'white','empty'],
                   ['empty', 'white', 'empty', 'white', 'empty','empty'],
                   ['empty', 'empty', 'white', 'empty', 'empty','empty'],
                   ['empty', 'empty', 'empty', 'white', 'empty','empty']]

WHITE_6SCORES = [50000, 5000, 5000, 500, 500, 100, 100, 100, 10, 10]

WHITE_5PATTERNS = [['white', 'white', 'white', 'white', 'white'],
                   ['white', 'white', 'white', 'white', 'empty'],
                   ['empty', 'white', 'white', 'white', 'white'],
                   ['white', 'white', 'empty', 'white', 'white'],
                   ['white', 'empty', 'white', 'white', 'white'],
                   ['white', 'white', 'white', 'empty', 'white']]
WHITE_5SCORES = [1000000, 5000, 5000, 5000, 5000, 5000]

BLACK_6PATTERNS = [['empty', 'black', 'black', 'black', 'black','empty'],
                   ['empty', 'black', 'black', 'black', 'empty','empty'],
                   ['empty', 'empty', 'black', 'black', 'black','empty'],
                   ['empty', 'black', 'black', 'empty', 'black','empty'],
                   ['empty', 'black', 'empty', 'black', 'black','empty'],
                   ['empty', 'empty', 'black', 'black', 'empty','empty'],
                   ['empty', 'empty', 'black', 'empty', 'black','empty'],
                   ['empty', 'black', 'empty', 'black', 'empty','empty'],
                   ['empty', 'empty', 'black', 'empty', 'empty','empty'],
                   ['empty', 'empty', 'empty', 'black', 'empty','empty']]
BLACK_6SCORES = [50000, 5000, 5000, 500, 500, 100, 100, 100, 10, 10]

BLACK_5PATTERNS = [['black', 'black', 'black', 'black', 'black'],
                   ['black', 'black', 'black', 'black', 'empty'],
                   ['empty', 'black', 'black', 'black', 'black'],
                   ['black', 'black', 'empty', 'black', 'black'],
                   ['black', 'empty', 'black', 'black', 'black'],
                   ['black', 'black', 'black', 'empty', 'black']]
BLACK_5SCORES = [1000000, 5000, 5000, 5000, 5000, 5000]


def sublist(ls1, ls2):
    """
    Return True if ls1 is a sublist of ls2.
    :param ls1: smaller list
    :param ls2: bigger list
    :return: Boolean representing if ls1 is a sublist of ls2
    """
    def get_all_in(one, another):
        for element in one:
            if element in another:
                yield element
    for x1, x2 in zip(get_all_in(ls1, ls2), get_all_in(ls2, ls1)):
        if x1 != x2:
            return False
    return True


def enum_to_string(vector):
    """
    Change BoardStates to the corresponding strings
    :param vector: vector of board states
    :return: vector of corresponding strings
    """
    string_list = []
    for item in vector:
        if item == BoardState.BLACK:
            string_list.append('black')
        elif item == BoardState.WHITE:
            string_list.append('white')
        else:
            string_list.append('empty')
    return string_list


def evaluate_vector(vector):
    """
    Returns the score of a vector
    :param vector: Vertical, horizontal or diagonal line
    :return: integer representing the score
    """
    string_list = enum_to_string(vector)
    score = {'white': 0, 'black': 0}
    length = len(string_list)

    if length == 5:
        for i in range(len(WHITE_5PATTERNS)):
            if WHITE_5PATTERNS[i] == string_list:
                score['white'] += WHITE_5SCORES[i]
            if BLACK_5PATTERNS[i] == string_list:
                score['black'] += BLACK_5SCORES[i]
        return score

    for i in range(length - 5):
        temp = [string_list[i], string_list[i + 1], string_list[i + 2], string_list[i + 3], string_list[i + 4]]
        for j in range(len(WHITE_5PATTERNS)):
            if WHITE_5PATTERNS[j] == temp:
                score['white'] += WHITE_5SCORES[j]
            if BLACK_5PATTERNS[j] == temp:
                score['black'] += BLACK_5SCORES[j]

    for i in range(length - 6):
        temp = [
            string_list[i],
            string_list[i + 1],
            string_list[i + 2],
            string_list[i + 3],
            string_list[i + 4],
            string_list[i + 5],
            ]
        for i in range(len(WHITE_6PATTERNS)):
            if WHITE_6PATTERNS[i] == temp:
                score['white'] += WHITE_6SCORES[i]
            if BLACK_6PATTERNS[i] == temp:
                score['black'] += BLACK_6SCORES[i]
    return score
